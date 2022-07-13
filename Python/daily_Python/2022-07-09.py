# Python CLI 를 위한 라이브러리 CLICK
# CLI 도구를 만들 때 가장 필요한 것은 옵션이나 인자를 처리하는 것

import click

@click.command()
@click.option('--count', default=1, help="Number of greetings")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo("Hello %s!" % name)

if __name__ == "__main__":
    hello()

"""
위의 파이썬 스크립트를 실행하면, @click.option 으로 지정해준대로 --count 옵션을 인자로 넣어서 실행함.
$ python 2022-07-09.py  --count=3
Your name: jaehun
Hello jaehun!
Hello jaehun!
Hello jaehun!
"""

# click.option 함수에 help 인자에 comment 를 입력하면, --help 사용시 comment 를 커맨드에서 확인 가능
