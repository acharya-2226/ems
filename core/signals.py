from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import transaction
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create appropriate profile when a new user is created.
    Handles both Student and Teacher profile creation based on user role.
    """
    if not created:
        return
    
    try:
        with transaction.atomic():
            # Check if user has role attribute
            if not hasattr(instance, 'role'):
                logger.warning(f"User {instance.id} created without role attribute")
                return
            
            if instance.role == 'student':
                _create_student_profile(instance)
            elif instance.role == 'teacher':
                _create_teacher_profile(instance)
            else:
                logger.info(f"User {instance.id} created with role '{instance.role}' - no profile needed")
                
    except Exception as e:
        logger.error(f"Error creating profile for user {instance.id}: {str(e)}")
        raise


def _create_student_profile(user):
    """Create student profile with auto-generated roll number."""
    from attendance.models import Student
    
    # Generate unique roll number
    roll_number = _generate_roll_number(user.id)
    
    student, created = Student.objects.get_or_create(
        user=user,
        defaults={
            'roll_number': roll_number,
            'is_active': True,
            
        }
    )
    
    if created:
        logger.info(f"Created student profile for user {user.id} with roll number {roll_number}")
    else:
        logger.warning(f"Student profile already exists for user {user.id}")


def _create_teacher_profile(user):
    """Create teacher profile."""
    from core.models import Teacher
    
    teacher, created = Teacher.objects.get_or_create(
        email=user.email,
        defaults={
            'name': user.get_full_name() or user.username,
            'is_active': True,
            'hire_date': user.date_joined.date() if user.date_joined else None
        }
    )
    
    # Link user to teacher if not already linked
    if not hasattr(user, 'teacher_profile'):
        # Assuming you have a OneToOne field from User to Teacher
        user.teacher_profile = teacher
        user.save()
    
    if created:
        logger.info(f"Created teacher profile for user {user.id}")


def _generate_roll_number(user_id, prefix="STD"):
    """Generate a unique roll number."""
    base_number = f"{prefix}{str(user_id).zfill(4)}"
    
    # Check for uniqueness (in case of ID conflicts)
    from attendance.models import Student
    counter = 0
    roll_number = base_number
    
    while Student.objects.filter(roll_number=roll_number).exists():
        counter += 1
        roll_number = f"{base_number}-{counter}"
    
    return roll_number


@receiver(pre_delete, sender=User)
def handle_user_deletion(sender, instance, **kwargs):
    """
    Handle cleanup when a user is deleted.
    Log the deletion and perform any necessary cleanup.
    """
    logger.info(f"User {instance.id} ({instance.username}) is being deleted")
    
    # Add any cleanup logic here if needed
    # For example, archiving related records instead of deleting them


# Additional signals for core models
@receiver(post_save, sender='core.Subject')
def subject_created(sender, instance, created, **kwargs):
    """Log when new subjects are created."""
    if created:
        logger.info(f"New subject created: {instance.code} - {instance.name}")


@receiver(post_save, sender='core.Teacher')
def teacher_status_changed(sender, instance, created, **kwargs):
    """Handle teacher status changes."""
    if not created:
        # If teacher is deactivated, you might want to handle their subjects
        if not instance.is_active:
            subjects_count = instance.subjects.count()
            if subjects_count > 0:
                logger.warning(
                    f"Teacher {instance.name} deactivated but still assigned to {subjects_count} subjects"
                )


@receiver(post_save, sender='core.Department')
def department_head_assigned(sender, instance, created, **kwargs):
    """Log when department head is assigned or changed."""
    if not created and instance.head:
        logger.info(f"Department head assigned: {instance.head.name} -> {instance.name}")


# Signal for handling room capacity changes
@receiver(post_save, sender='core.Room')
def room_capacity_changed(sender, instance, created, **kwargs):
    """Log room capacity changes for scheduling implications."""
    if not created:
        # You could add logic here to check if room capacity change affects existing schedules
        logger.info(f"Room {instance.name} capacity updated to {instance.capacity}")


@receiver(pre_delete, sender='core.Subject')
def subject_deletion_check(sender, instance, **kwargs):
    """
    Log subject deletions and check for dependencies.
    """
    logger.warning(f"Subject being deleted: {instance.code} - {instance.name}")
    
    # Check if subject is a prerequisite for other subjects
    dependent_subjects = instance.prerequisite_for.all()
    if dependent_subjects.exists():
        dependent_names = [s.code for s in dependent_subjects]
        logger.warning(
            f"Subject {instance.code} is prerequisite for: {', '.join(dependent_names)}"
        )