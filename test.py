import unittest
from app import app, db
from app.models import Todo, Deleted

class TestTodoApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_add_task(self):
        with app.app_context():  # Create the application context
            data = {'title': 'Task 1', 'description': 'Description 1'}
            response = self.app.post('/add', data=data)
            self.assertEqual(response.status_code, 302)  # Redirect status code

            # Access the database model within the application context
            task = Todo.query.filter_by(title='Task 1').first()
            self.assertIsNotNone(task)
            self.assertEqual(task.description, 'Description 1')
            self.assertFalse(task.complete)

    def test_complete_task(self):
        # Add a task to the database
        with app.app_context():
            new_task = Todo(title='Task 2', description='Description 2')
            db.session.add(new_task)
            db.session.commit()

            response = self.app.get(f'/complete/{new_task.id}')
            self.assertEqual(response.status_code, 302)  # Redirect status code

            # Check if the task is marked as completed in the database
            task = Todo.query.filter_by(id=new_task.id).first()
            self.assertTrue(task.complete)
    
    def test_delete_task(self):
        # Add a task to the database
        with app.app_context():
            new_task = Todo(title='Task 3', description='Description 3')
            db.session.add(new_task)
            db.session.commit()

            response = self.app.get(f'/delete/{new_task.id}')
            self.assertEqual(response.status_code, 302)  # Redirect status code

            # Check if the task is marked as deleted in the database
            task = Todo.query.filter_by(id=new_task.id).first()
            self.assertIsNone(task)  # The task should be deleted from the Todo table

            # Check if the task is added to the Deleted table
            deleted_task = Deleted.query.filter_by(id=new_task.id).first()
            self.assertIsNotNone(deleted_task)
            self.assertEqual(deleted_task.title, 'Task 3')
            self.assertEqual(deleted_task.description, 'Description 3')
    
if __name__ == '__main__':
    unittest.main()
