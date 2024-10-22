describe('addMarkup', () => {
  it('creates correct markup for a book', () => {
    const book = {
      id: '123',
      thumbnail: 'test.jpg',
      title: 'Test Book',
      authors: 'Test Author',
      publishedDate: '2024',
      description: 'Test description'
    };

    const result = addMarkup(book);
    expect(result.hasClass('list-group-item')).toBeTruthy();
    expect(result.html()).toContain(book.title);
    expect(result.html()).toContain(book.authors);
  });
});

describe('convertSearchString', () => {
  it('converts spaces to plus signs outside quotes', () => {
    expect(convertSearchString('test search')).toBe('test+search');
  });

  it('preserves spaces inside quotes', () => {
    expect(convertSearchString('"test search" query')).toBe('"test search"+query');
  });

  it('empty string', () => {
    expect(convertSearchString('')).toBe('');
  });

  it('string with only quotes', () => {
    expect(convertSearchString('""')).toBe('""');
  });
});


// How to test the API call? Create a fake reply? That would be needed for the updateBookSearch.

// Event listeners can be tested selecting the triggering a click, how to check for shown or hidden?