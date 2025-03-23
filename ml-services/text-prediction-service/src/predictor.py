'''Module for Bert Model Predictor  Class'''

import string
import torch
from transformers import BertTokenizer, BertForMaskedLM

TOP_K = 10

class Predictor:
    '''Predictor Class'''
    def __init__(self):
        self.bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.bert_model = BertForMaskedLM.from_pretrained('bert-base-uncased').eval()

    def decode(self,tokenizer, pred_idx, top_clean):
        '''Token Decode Function'''
        ignore_tokens = string.punctuation + '[PAD]'
        tokens = []
        for w in pred_idx:
            token = ''.join(tokenizer.decode(w).split())
            if token not in ignore_tokens:
                tokens.append(token.replace('##', ''))
        return '\n'.join(tokens[:top_clean])

    def encode(self, tokenizer, text_sentence, add_special_tokens=True):
        '''Token Encode Function'''
        text_sentence = text_sentence.replace('<mask>', tokenizer.mask_token)
        if tokenizer.mask_token == text_sentence.split()[-1]:
            text_sentence += ' .'

        input_ids = torch.tensor([tokenizer.encode(text_sentence, add_special_tokens=add_special_tokens)])
        mask_idx = torch.where(input_ids == tokenizer.mask_token_id)[1].tolist()[0]
        return input_ids, mask_idx

    def get_all_predictions(self, text_sentence, top_clean=5):
        '''Next Word Predictions '''
        input_ids, mask_idx = self.encode(self.bert_tokenizer, text_sentence)
        with torch.no_grad():
            predict = self.bert_model(input_ids)[0]
        predicted_words = self.decode(self.bert_tokenizer, predict[0, mask_idx, :].topk(TOP_K).indices.tolist(), top_clean)
        return predicted_words

    def gen_m_words_n_predictions(self, m, n, input_text):
        '''N-Word Predictions'''
        output = []
        res = self.get_all_predictions(input_text + ' <mask>', top_clean=n).split('\n')
        input_text_copy = input_text
        for i in res:
            input_text = input_text_copy + ' ' + i
            for i in range(m-1):
                word = self.get_all_predictions(input_text + ' <mask>', top_clean=1).split('\n')
                input_text = input_text+ ' ' + word[0]
            output.append(input_text)
        return output