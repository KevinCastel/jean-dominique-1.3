class Correction:
    def __init__(self, input_to_correct:str):
        self._dict_model = {
            "demarrer" : False,
            "multi" : False,
            "jouer" : False,
            "stop" : False,
            "uninstall" : False,
            "reinstall" : False,
            "play" : False,
            "solo" : False,
            "stop" : False
        }
        self._input = input_to_correct

    def set_correction(self):
        list_words = []
        word = self._input
        if " " in word: word.replace(" ")
        prediction = ""
        is_prediction_reliable = False
        
        for c in self._input:
            word += c
            prediction = self._test_word_by_model(word)
            
            if len(prediction) > 0:
                is_prediction_reliable = self._check_prediction(prediction)
                if is_prediction_reliable:
                    list_words.append(prediction)
                    prediction = ""
    
    def _check_prediction(self, p:str):
        return (p in self._dict_model)
    
    def _test_word_by_model(self, word:str):
        list_c = []; prediction = ""
        foundt = False
        prob = 0
        for m in self._dict_model:
            list_c = self._get_list_chars_from_model(m)
            index = 0
            prediction = ""
            for c in word:
                if c in list_c:
                    if c == list_c[index]:
                        prediction += c
                index += 1
        return prediction
    
    def _get_list_chars_from_model(self, model:str):
        list_chars = ""
        for c in model:
            if not c in list_chars:
                list_chars.append(c)
        return list_chars