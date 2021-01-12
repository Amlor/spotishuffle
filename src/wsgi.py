from src.server import create_app

if __name__ == "__main__":
    application = create_app('src.config')
    application.run()