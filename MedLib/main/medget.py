import infermedica_api

infermedica_api.configure(app_id='349a2f56', app_key='cca4f464530bc1b49433057c2470fd44')

class medget:

    api = infermedica_api.get_api()

    def get_data(self,sex_m,age_m):

        self.user_data = infermedica_api.Diagnosis(sex=sex_m, age=age_m)
        
    
    def add_symptoms(self, ids):
        
        for i in ids:
            self.user_data.add_symptom( i['id'], i['status'])
        #absent status add

    def search_symptoms(self, symptoms_str):
        search_res = []
        #global api
        #j=0
        for i in symptoms_str:
            res = self.api.search(i)

            #j = 0
            for k in res:
                res_p = {}
                res_p['id'] = str(k[str('id')])
                res_p['label'] = str(k[str('label')])
                search_res.append(res_p)
                res_p=None
                #j = j + 1

        #return self.api.search('headache')
        return search_res

    def get_question(self, ):
        self.user_data = self.api.diagnosis(self.user_data)
        ques = {}

        ques['text'] = self.user_data.question.text
        ques['text'] = self.user_data.question.text
        ques['id'] = self.user_data.question.items[0]['id']
        ques['name'] = self.user_data.question.items[0]['name']
        return ques

    def check_risk(self, ):
        if self.user_data.conditions[0]['probability'] > 0.7:
            return 1
        else:
            return 0

    def get_result(self, ):
        result = {}
        result['id'] = str(self.user_data.conditions[0][str('id')])      
        result['name'] = str(self.user_data.conditions[0][str('name')])
        result['prob'] = str(self.user_data.conditions[0]['probability'])
        k = self.api.condition_details(result['id']).__dict__
        result['hint'] = str(k[str('extras')][str('hint')])
        result['severity'] = str(k[str('severity')])
        result['prevalence'] = str(k[str('prevalence')])
        result['acuteness'] = str(k[str('acuteness')])
        return result
 
'''
print(request.question.text)  # actual text of the question

print '*************hey 6*********************'

print(request.question.items)  # list of related evidences with possible answers

print '*************hey 7*********************'

print(request.question.items[0]['id'])

print '*************hey 8*********************'

print(request.question.items[0]['name'])

'''

