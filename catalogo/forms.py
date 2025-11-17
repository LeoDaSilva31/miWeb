"""
Formularios para productos de Supabase
"""
from django import forms
from miwebsite.image_utils import validate_image_file

class ProductoSupabaseForm(forms.Form):
    """
    Formulario para crear/editar productos en Supabase
    """
    titulo = forms.CharField(
        max_length=200,
        label="Título",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Título del producto'
        })
    )
    
    descripcion = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Descripción del producto'
        })
    )
    
    precio = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Precio",
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01'
        })
    )
    
    foto = forms.ImageField(
        label="Foto",
        required=False,
        help_text="Imagen será automáticamente optimizada y convertida a WebP (máximo 2MB)",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )
    
    activo = forms.BooleanField(
        label="Activo",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    orden = forms.IntegerField(
        label="Orden",
        initial=0,
        help_text="Número para ordenar los productos",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0'
        })
    )
    
    def clean_foto(self):
        """Validar el archivo de imagen"""
        foto = self.cleaned_data.get('foto')
        
        if foto:
            # Validar que sea una imagen
            if not validate_image_file(foto):
                raise forms.ValidationError("El archivo debe ser una imagen válida (JPEG, PNG, GIF, BMP, WebP)")
            
            # Validar tamaño máximo antes del procesamiento (10MB como límite inicial)
            max_size = 10 * 1024 * 1024  # 10MB
            if foto.size > max_size:
                raise forms.ValidationError("La imagen es demasiado grande. Máximo 10MB")
        
        return foto
    
    def clean_precio(self):
        """Validar precio"""
        precio = self.cleaned_data.get('precio')
        
        if precio is not None and precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo")
        
        return precio


# ============================================================
#  Formulario para comentarios en productos
# ============================================================

from .models import ProductoComentario


class ProductoComentarioForm(forms.ModelForm):
    """Formulario para crear comentarios en productos."""
    
    class Meta:
        model = ProductoComentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'maxlength': '200',
                'placeholder': 'Escribí tu comentario (máximo 200 caracteres)',
                'rows': 2,
                'class': 'form-control',
            })
        }
    
    def clean_texto(self):
        texto = self.cleaned_data.get('texto', '').strip()
        if not texto:
            raise forms.ValidationError("El comentario no puede estar vacío.")
        if len(texto) > 200:
            raise forms.ValidationError("El comentario no puede exceder 200 caracteres.")
        return texto