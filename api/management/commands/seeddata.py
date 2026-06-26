from django.core.management.base import BaseCommand
from api.models import Usuario, Curso
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Seed the database with users and courses'

    def handle(self, *args, **options):
        users_data = [
            {'username': 'admin', 'email': 'admin@curxo.com', 'password': 'admin123', 'first_name': 'Admin', 'last_name': 'CURXO', 'rol': 'admin', 'is_superuser': True, 'is_staff': True},
            {'username': 'estudiante', 'email': 'estudiante@curxo.com', 'password': 'test123', 'first_name': 'Juan', 'last_name': 'Perez', 'rol': 'estudiante'},
            {'username': 'profesor', 'email': 'profesor@curxo.com', 'password': 'test123', 'first_name': 'Maria', 'last_name': 'Garcia', 'rol': 'profesor'},
            {'username': 'estudiante2', 'email': 'estudiante2@curxo.com', 'password': 'test123', 'first_name': 'Carlos', 'last_name': 'Lopez', 'rol': 'estudiante'},
            {'username': 'profesor2', 'email': 'profesor2@curxo.com', 'password': 'test123', 'first_name': 'Ana', 'last_name': 'Martinez', 'rol': 'profesor'},
        ]

        created_users = []
        for u in users_data:
            is_su = u.pop('is_superuser', False)
            try:
                if is_su:
                    user = Usuario.objects.create_superuser(**u)
                else:
                    user = Usuario.objects.create_user(**u)
                created_users.append(user)
                self.stdout.write(self.style.SUCCESS(f'Created user: {user.email}'))
            except IntegrityError:
                user = Usuario.objects.get(email=u['email'])
                created_users.append(user)
                self.stdout.write(f'User already exists: {user.email}')
            u['is_superuser'] = is_su

        self.stdout.write(self.style.SUCCESS(f'Total users: {Usuario.objects.count()}'))

        profesor_u = created_users[2]
        profesor2_u = created_users[4]

        courses_data = [
            {'titulo': 'Desarrollo Web Full Stack', 'descripcion': 'Aprende HTML, CSS, JavaScript, React y Node.js desde cero.', 'profesor': profesor_u, 'precio': 199.99, 'duracion_horas': 120, 'nivel': 'intermedio'},
            {'titulo': 'Python para Data Science', 'descripcion': 'Domina Python, Pandas, NumPy y Machine Learning.', 'profesor': profesor_u, 'precio': 249.99, 'duracion_horas': 80, 'nivel': 'avanzado'},
            {'titulo': 'Diseno UX/UI', 'descripcion': 'Crea interfaces de usuario atractivas y funcionales.', 'profesor': profesor2_u, 'precio': 149.99, 'duracion_horas': 60, 'nivel': 'basico'},
            {'titulo': 'Ciberseguridad Basica', 'descripcion': 'Protege sistemas y redes contra amenazas digitales.', 'profesor': profesor2_u, 'precio': 179.99, 'duracion_horas': 50, 'nivel': 'basico'},
            {'titulo': 'DevOps y CI-CD', 'descripcion': 'Automatiza el desarrollo y despliegue de software.', 'profesor': profesor_u, 'precio': 299.99, 'duracion_horas': 70, 'nivel': 'avanzado'},
            {'titulo': 'App Moviles con Flutter', 'descripcion': 'Desarrolla apps nativas para iOS y Android.', 'profesor': profesor2_u, 'precio': 219.99, 'duracion_horas': 90, 'nivel': 'intermedio'},
            {'titulo': 'Cloud Computing AWS', 'descripcion': 'Infraestructura en la nube con servicios de Amazon.', 'profesor': profesor_u, 'precio': 259.99, 'duracion_horas': 85, 'nivel': 'avanzado'},
            {'titulo': 'Inteligencia Artificial', 'descripcion': 'Fundamentos de IA, redes neuronales y deep learning.', 'profesor': profesor2_u, 'precio': 299.99, 'duracion_horas': 100, 'nivel': 'avanzado'},
        ]

        for c in courses_data:
            try:
                Curso.objects.create(**c)
                self.stdout.write(self.style.SUCCESS(f'Created course: {c["titulo"]}'))
            except IntegrityError:
                self.stdout.write(f'Course already exists: {c["titulo"]}')

        self.stdout.write(self.style.SUCCESS(f'Total courses: {Curso.objects.count()}'))
