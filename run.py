from flask_blog_project import create_app


# создание объекта приложения
app = create_app()


# запуск как главная программа
if __name__ == '__main__':
    app.run(debug=True)

