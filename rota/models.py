from django.db import models

# Create your models here.
class Rota(models.Model):
    """
    Define a rota de onibus
    """
    nome = models.CharField(
        max_length=200,
        help_text="Nome ou identificador da rota"
    )

    ativo = models.BooleanField(
        default=True,
        help_text="Indica se a rota esta na operação"
    )

    class Meta:
        verbose_name = "Rota"
        verbose_name_plural = "Rotas"
        ordering = ['nome']

    def __str__(self):
        return self.nome
    
class Parada(models.Model):
    """
    Define um ponto de parada de ônibus.
    """
    endereco = models.CharField(
        max_length=255, 
        help_text="Descrição do endereço ou nome da parada"
    )

    latitude_longitude = models.CharField(
        max_length=50, 
        help_text="Coordenadas no formato 'latitude,longitude' (ex: -24.7988039,-49.9928598)"
    )

    ativo = models.BooleanField(
        default=True,
        help_text="Indica se a parada está atualmente em uso"
    )

    class Meta:
        verbose_name = "Parada"
        verbose_name_plural = "Paradas"
        ordering = ['endereco']

    def __str__(self):
        return self.endereco
    

class RotaParadaHorario(models.Model):
    """
    Tabela associativa (Through table) que conecta Rotas e Paradas,
    especificando o horário e o status de atividade dessa conexão.
    """
    rota = models.ForeignKey(
        Rota, 
        on_delete=models.CASCADE,
        related_name="horarios_parada"
    )
    parada = models.ForeignKey(
        Parada, 
        on_delete=models.CASCADE,
        related_name="horarios_rota"
    )
    horario = models.TimeField(
        help_text="Horário programado para a passagem do ônibus nesta parada"
    )
    ativo = models.BooleanField(
        default=True,
        help_text="Indica se este horário específico nesta parada/rota está ativo"
    )

    class Meta:
        verbose_name = "Horário da Rota na Parada"
        verbose_name_plural = "Horários das Rotas nas Paradas"
        
        # Garante que não haja um horário duplicado para a mesma parada na mesma rota
        unique_together = ('rota', 'parada', 'horario')
        
        # Classifica/Ordena os registros primeiro pela Rota, e depois pelo Horário
        ordering = ['rota', 'horario']

    def __str__(self):
        # Verifica o status de todos os objetos relacionados
        rota_nome = self.rota.nome if self.rota else "Rota Indefinida"
        parada_end = self.parada.endereco if self.parada else "Parada Indefinida"
        horario_str = self.horario.strftime('%H:%M') if self.horario else "HH:MM"
        
        status_horario = "Ativo" if self.ativo else "Inativo"
        
        return (f"Rota: {rota_nome} | "
                f"Parada: {parada_end} | "
                f"Horário: {horario_str} ({status_horario})")