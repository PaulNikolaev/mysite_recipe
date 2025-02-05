from uuid import uuid4
from pytils.translit import slugify


def unique_slugify(instance, slug, slug_field):
    """
    Генератор уникальных SLUG для моделей, в случае существования такого SLUG.
    """
    model = instance.__class__
    base_slug = slugify(slug)

    if slug_field:
        base_slug = slug_field

    unique_slug = base_slug
    counter = 1

    while model.objects.filter(slug=unique_slug).exclude(id=instance.id).exists():
        unique_slug = f"{base_slug}-{uuid4().hex[:8]}"
        counter += 1

    return unique_slug