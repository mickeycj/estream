from mamba import description, it
from expects import equal, expect

def say_hello_to(name):
    return f'Hello, {name}'

with description('Hello') as self:
    with it('says hello to the world'):
        # Given
        name = 'World'
        # When
        hello_str = say_hello_to(name)
        # Then
        expect(hello_str).to(equal('Hello, World'))
