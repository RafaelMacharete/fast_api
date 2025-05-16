
'''

def fake_db():
    try:
        print("Connecting to DATABASE")
    finally:
        print("Ending connetion to DATABASE")
        

@app.get('/')
async def root():
    return {'msg:': 'It works!!!'}


@app.get('/characters', description='Return all characters on database')
async def get_characters():
    return characters
    

@app.get('/characters/{character_id}')
async def get_character_by_id(character_id:int):
    try:
        character = characters[character_id]
        return character
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Does not exist a character with id: {character_id}')
        

@app.post('/characters', status_code=status.HTTP_201_CREATED)
async def post_character(character: Optional[Character] = None):
    next_id = len(characters) + 1
    characters[next_id] = character
    del character.id
    return character


@app.put('/characters/{character.id}', status_code=status.HTTP_202_ACCEPTED)
async def put_character(character_id:int, character: Character):
    if character_id in characters:
        characters[character_id] = character
        character.id = character_id
        del character.id
        return character
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Does not exist a character with id: {character_id}')
        

@app.delete('/characters/{character_id}')
async def delete_character(character_id:int):
    if character_id in characters:
        del characters[character_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Does not exist a character with id: {character_id}')


@app.get('/calculator')
async def calculate(first_number: int, second_number:int):
    sum = first_number + second_number

    return sum


@app.get('/characters')
async def get_characters(db: Any = Depends(fake_db)):
    return characters
'''

    
if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run('main:app', host='localhost', port=8000, log_level='info', reload=True)