from .models import IHAPiece

def get_part_count_for_model(model_type, part_type):
    return IHAPiece.objects.filter(model_type=model_type, piece_type=part_type).count()
