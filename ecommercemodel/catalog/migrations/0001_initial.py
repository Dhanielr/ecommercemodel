# Generated by Django 2.2.5 on 2019-12-27 19:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('slug', models.SlugField(max_length=100, verbose_name='Identificador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Código')),
                ('name', models.CharField(help_text='Obrigatório. Nome do Produto, de maior destaque na página.', max_length=100, verbose_name='Nome')),
                ('slug', models.SlugField(help_text='Não alterar esse campo.', max_length=100, verbose_name='Identificador')),
                ('description', models.TextField(help_text='Obrigatório. Uma descrição breve do Produto. Max. 85 caracteres.', max_length=85, verbose_name='Descrição')),
                ('description_big', models.TextField(blank=True, help_text='Opcional. Uma descrição longa do Produto. Max. 800 caracteres.', max_length=800, null=True, verbose_name='Descrição Detalhada')),
                ('price', models.DecimalField(decimal_places=2, help_text='Obrigatório. Determine um preço para o Produto.', max_digits=8, verbose_name='Preço')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('thumbnail', models.ImageField(help_text='Obrigatório. Envie uma imagem para ser Thumbnail no produto. Thumbnails aparecem primeiro.', upload_to='products', verbose_name='Thumbnail do Produto')),
                ('image2', models.ImageField(blank=True, help_text='Opcional. Envie aqui fotos adicionais do produto.', null=True, upload_to='products', verbose_name='Imagem2')),
                ('image3', models.ImageField(blank=True, help_text='Opcional. Envie aqui fotos do produto.', null=True, upload_to='products', verbose_name='Imagem3')),
                ('image4', models.ImageField(blank=True, help_text='Opcional. Envie aqui fotos do produto.', null=True, upload_to='products', verbose_name='Imagem4')),
                ('start_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='Opcional, defina uma data futura, para que o Produto seja exibido somente a partir dela.', null=True, verbose_name='Data de Exibição')),
                ('end_date', models.DateTimeField(blank=True, help_text='Opcional, defina uma data futura, para que o Produto deixe de ser exibido a partir dela.', null=True, verbose_name='Data de Expiração')),
                ('is_active', models.BooleanField(default=True, help_text='Determina se esse Produto deve ser tratado como ativo. Desmarque isso em vez de excluir produtos.', verbose_name='Ativo')),
                ('spotlight', models.BooleanField(default=False, help_text='Determina se esse Produto deve ser tratado como Destaque. Geralmente produtos em destaque possuem promoções.', verbose_name='Destaque')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criado_por', to=settings.AUTH_USER_MODEL, verbose_name='Criado por')),
                ('category', models.ForeignKey(help_text='Determine a categoria do produto.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Categoria', to='catalog.Category', verbose_name='Categoria')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'ordering': ['name'],
            },
        ),
    ]
