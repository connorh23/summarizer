import streamlit 

import file_utils

HIGHLIGHT = 'highlight'
TRIM = 'trim'

SUMMARIZATION_MODE = [HIGHLIGHT, TRIM]


def compile_summarized_markdown(raw_sentences, summary_sentence_indexes, mode):

    markdown = ''

    for i in range(len(raw_sentences)):

        if mode is HIGHLIGHT:
            if i in summary_sentence_indexes:
                markdown += '  ***' + raw_sentences[i] + '***'
            else:
                markdown += raw_sentences[i]

        elif mode is TRIM:
            if i in summary_sentence_indexes:
                markdown += '  ' + raw_sentences[i]

    return markdown

def transform_slider_input(x):
    return str(int(x/10))

# Read processed summary file
manifest = file_utils.read_json('summary_output.json')

# Get specific pieces of data
audio_url = manifest['audio_url']
sentences = manifest['sentences']
summary_indices = manifest['summary_indices']


# ========== UI ==================================================

streamlit.title('Audio Summarizer')

# Audio Player
streamlit.markdown('## Original Audio')
streamlit.audio(audio_url, format='audio/mp3', start_time=0)

# Horizontal Divider
streamlit.markdown('***')

# Summarization Slider
streamlit.markdown("## Summarization Level")
x = streamlit.slider(label='(% of original text)', min_value=10, max_value=90, value=50, step=10)

# Get summarization mode
mode = streamlit.radio('Summarization Mode', [HIGHLIGHT, TRIM], index=0)

# Horizontal Divider
streamlit.markdown('***')

# Get summary sentences
x = transform_slider_input(x)
summary_sentence_indexes = summary_indices[x]
markdown = compile_summarized_markdown(sentences, summary_sentence_indexes, mode)

# Transcription + Summary
streamlit.markdown(markdown)



