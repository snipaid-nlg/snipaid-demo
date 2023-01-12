from django.shortcuts import render
import banana_dev as banana
from django.http import JsonResponse
from django.conf import settings


# Generate a headline or teaser depending on gen_type parameter with a given fulltext
def generate(request):
  fulltext = request.GET.get('fulltext')
  gen_type = request.GET.get('gen_type')

  # General settings
  model_inputs = {
    "temperature": 1.0, 
    "top_p": 0.7,
    "num_beams": 1,
    "do_sample": True
  }

  # Specific settings for headline generation
  if gen_type == 'headline':
    model_inputs["prompt"] = f'[Text]:{fulltext}\n\n[Titel]:'
    model_inputs["max_new_tokens"] = 60
  # Specific settings for teaser generation
  elif gen_type == 'teaser':
    model_inputs["prompt"] = f'[Text]:{fulltext}\n\n[Teaser]:'
    model_inputs["max_new_tokens"] = 150

  out = banana.run(settings.BANANA_API_KEY, settings.BANANA_MODEL_KEY, model_inputs)
  output = out['modelOutputs'][0]['output']

  
  # Specific text cleaning for headlines
  if gen_type == 'headline':
    output = output.split("[Titel]:")[1]
    output = output.split('\n')[0]
    output = output.split('.')[0]
    output = output.split('?')[0]
    output = output.split('!')[0]
  # Specific text cleaning for teasers
  elif gen_type == 'teaser':
    output = output.split("[Teaser]:")[1]
    output = ".".join(output.split('.')[:-1])
    output += '.'
  
  # General text cleaning
  output = output.replace('\n', ' ')
  while '\s\s' in output:
    output = output.replace('\s\s', '\s')
  output = output.strip()
  
  

  return JsonResponse({"output": output})