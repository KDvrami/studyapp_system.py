from sub_app import sub_app
import os

app = sub_app()

if __name__ == "__main__":
    app.run(debug=os.getenv('DEBUG', 'False').lower() in ['true', '1', 't'])