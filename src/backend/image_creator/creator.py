import imgkit
from jinja2 import Environment, FileSystemLoader

if __name__ == '__main__':
    loader = FileSystemLoader('./templates')
    env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('test.html')

    k = template.render(name='Григорий', right=10, all=16, text='Родительный падеж')
    imgkit.from_string(k, 'out.jpg', css='./styles/style.css')


