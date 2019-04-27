import imgkit
from jinja2 import Environment, FileSystemLoader


class HTMLConventor:
    def __init__(self, html_name):
        self.loader = FileSystemLoader('./templates')
        self.env = Environment(loader=self.loader, trim_blocks=True, lstrip_blocks=True)
        self.template = self.env.get_template(html_name)

    @staticmethod
    def render(name, right, all, text):
        k = template.render(name=name, right=right, all=all, text=text)
        imgkit.from_string(k, 'out.jpg', css='./styles/style.css')


if __name__ == '__main__':
    loader = FileSystemLoader('./templates')
    env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('test.html')

    k = template.render(name='Григорий', right=10, all=16, text='Родительный падеж')
    imgkit.from_string(k, 'out.jpg', css='./styles/style.css')
