localized = True
#default_locale is 'en_US' in the previous State of this application
default_locale = 'la' 
#external provider
external_provider = ''

from .. import BaseProvider


class Provider(BaseProvider):
    '''
    factory.create will enter this class and will and will list all the
    methods then will go to 'la.__init__'

    Why does it goes to 'la' as soon as it finish to read this class
    '''
    #import pytest; pytest.set_trace()
    word_connector = ' '
    sentence_punctuation = '.'
    @classmethod
    def word(cls, ext_word_list=None):
        """
        Generate a random word
        :example 'lorem'

        Keyword arguments:
        'ext_word_list' --- a list of word you would like to have 
                 instead of 'Lorem ipsum'
        """
        if ext_word_list:
            return cls.random_element(ext_word_list)
        return cls.random_element(cls.word_list)

    @classmethod
    def words(cls, nb=3, ext_word_list=None):
        """
        Generate an array of random words
        :example array('Lorem', 'ipsum', 'dolor')

        Keyword arguments:
        nb --- how many words to return
        'ext_word_list' --- a list of word you would like to have 
                 instead of 'Lorem ipsum'
        """
        if ext_word_list:
            return [cls.word(ext_word_list) for _ in range(0, nb)]
        return [cls.word() for _ in range(0, nb)]

    @classmethod
    def sentence(cls, nb_words=6, variable_nb_words=True, ext_word_list=None):
        """
        Generate a random sentence
        :example 'Lorem ipsum dolor sit amet.'

        Keyword arguments:
        :param 'nb_words' --- around how many words the sentence should contain
        :param 'variable_nb_words' --- set to false if you want exactly $nbWords returned,
            otherwise $nbWords may vary by +/-40% with a minimum of 1
        :param 'ext_word_list' --- a list of word you would like to have 
                 instead of 'Lorem ipsum'
        """
        if nb_words <= 0:
            return ''

        if variable_nb_words:
            nb_words = cls.randomize_nb_elements(nb_words)

        if ext_word_list:
            words = cls.words(nb_words, ext_word_list)
        else:
            words = cls.words(nb_words)
        words[0] = words[0].title()

        return cls.word_connector.join(words) + cls.sentence_punctuation

    @classmethod
    def sentences(cls, nb=3, ext_word_list=None):
        """
        Generate an array of sentences
        :example array('Lorem ipsum dolor sit amet.', 'Consectetur adipisicing eli.')

        Keyword arguments:
        :param 'nb'--- how many sentences to return
        :param 'ext_word_list'--- a list of word you would like to have 
                 instead of 'Lorem ipsum'

        :return list
        """
        if ext_word_list:
            return [cls.sentence(ext_word_list=ext_word_list) for _ in range(0, nb)]
        return [cls.sentence() for _ in range(0, nb)]

    @classmethod
    def paragraph(cls, nb_sentences=3, variable_nb_sentences=True, ext_word_list=None):
        """
        Generate a single paragraph
        :example 'Sapiente sunt omnis. Ut pariatur ad autem ducimus et. Voluptas rem voluptas sint modi dolorem amet.'

        Keyword arguments:
        :param 'nb_sentences' --- around how many sentences the paragraph should contain
        :param 'variable_nb_sentences' --- set to false if you want exactly $nbSentences returned,
            otherwise $nbSentences may vary by +/-40% with a minimum of 1
        :param 'ext_word_list' --- a list of word you would like to have 
                 instead of 'Lorem ipsum'

        :return string
        """
        if nb_sentences <= 0:
            return ''

        if variable_nb_sentences:
            nb_sentences = cls.randomize_nb_elements(nb_sentences)

        if ext_word_list:
            return cls.word_connector.join(cls.sentences(
                nb_sentences, ext_word_list=ext_word_list)
                )

        return cls.word_connector.join(cls.sentences(nb_sentences))

    @classmethod
    def paragraphs(cls, nb=3, ext_word_list=None):
        """
        Generate an array of paragraphs
        :example array($paragraph1, $paragraph2, $paragraph3)
        :param nb how many paragraphs to return
        :param 'ext_word_list' a list of word you would like to have 
                 instead of 'Lorem ipsum'
        :return array
        """
        if ext_word_list:
            return [cls.paragraph(ext_word_list=ext_word_list) for _ in range(0, nb)]

        return [cls.paragraph() for _ in range(0, nb)]

    @classmethod
    def text(cls, max_nb_chars=200, ext_word_list=None):
        """
        Generate a text string.
        Depending on the $maxNbChars, returns a string made of words, sentences, or paragraphs.
        :example 'Sapiente sunt omnis. Ut pariatur ad autem ducimus et. Voluptas rem voluptas sint modi dolorem amet.'

        Keyword arguments:
        :param 'max_nb_chars' --- Maximum number of characters the text should contain (minimum 5)
        :param 'ext_word_list' --- a list of word you would like to have 
                 instead of 'Lorem ipsum'

        :return string
        """
        text = []
        if max_nb_chars < 5:
            raise ValueError('text() can only generate text of at least 5 characters')

        if max_nb_chars < 25:
            # join words
            while not text:
                size = 0
                # determine how many words are needed to reach the $max_nb_chars once;
                while size < max_nb_chars:
                    if ext_word_list:
                        word = (cls.word_connector if size else '') + cls.word(ext_word_list=ext_word_list)
                    else:
                        word = (cls.word_connector if size else '') + cls.word()
                    text.append(word)
                    size += len(word)
                text.pop()
            text[0] = text[0][0].upper() + text[0][1:]
            last_index = len(text) - 1
            text[last_index] += cls.sentence_punctuation
        elif max_nb_chars < 100:
            # join sentences
            while not text:
                size = 0
                # determine how many sentences are needed to reach the $max_nb_chars once
                while size < max_nb_chars:
                    if ext_word_list:
                        sentence = (cls.word_connector if size else '') + cls.sentence(ext_word_list=ext_word_list)
                    else:
                        sentence = (cls.word_connector if size else '') + cls.sentence()
                    text.append(sentence)
                    size += len(sentence)
                text.pop()
        else:
            # join paragraphs
            while not text:
                size = 0
                # determine how many paragraphs are needed to reach the $max_nb_chars once
                while size < max_nb_chars:
                    if ext_word_list:
                        paragraph = ('\n' if size else '') + cls.paragraph(ext_word_list=ext_word_list)
                    else:
                        paragraph = ('\n' if size else '') + cls.paragraph()
                    text.append(paragraph)
                    size += len(paragraph)
                text.pop()

        return "".join(text)
