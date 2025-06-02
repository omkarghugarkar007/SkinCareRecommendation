import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv() 

def callLLM(prompt):

  client = OpenAI()

  response = client.responses.create(
      model="gpt-4o-mini",
      input=prompt,
      temperature=0
  )

  return response.output_text

def findIntent(query):

  prompt = f"""
  Classify the following user query as either “Recommendation” or “Non-Recommendation.”

  Examples:
  Input: “How is this serum for sensitive skin?”
  Output: Non-Recommendation

  Input: “serums”
  Output: Recommendation

  Input: “something gentle for summer”
  Output: Recommendation

  Input: “I want to buy face-wash”
  Output: Recommendation

  Input: “What happened to my user ticket”
  Output: Non-Recommendation

  Now classify:
  Input: “{query}”
  Output:
  """

  return callLLM(prompt)

def recommQuestion(query):

  prompt = f"""
  You are a helpful and friendly assistant that, when presented with a recommendation-style query, first asks 2–3 short, contextual follow-up questions to understand the user’s needs before showing any results. Follow the patterns below.

  Examples:

  ### Example 1: Specific Keyword
  User Query: “serums”  
  Assistant (ask follow-ups):
  1. Great choice! What skin concern are you targeting—hydration, blemishes, or something else?  
  2. And could you tell me about your skin type—oily, acne-prone, or dry and flaky?  

  ### Example 2: Vague Request
  User Query: “something gentle for summer”  
  Assistant (ask follow-ups):
  1. What product category are you interested in—toners, serums, SPFs, or cleansers?  
  2. Do you have any specific skin concerns or ingredients you’d like to avoid?  
  3. Finally, is there a particular texture or finish you prefer—lightweight gel, creamy, or spray?  

  ### Example 3: Another Specific Keyword
  User Query: “moisturizers”  
  Assistant (ask follow-ups):
  1. Perfect—what’s your main goal: extra hydration, oil control, or anti-aging?  
  2. How would you describe your skin type—combination, sensitive, or normal?  
  3. Any ingredients you love or dislike (like hyaluronic acid, ceramides, or fragrances)?  

  ---

  Now apply this pattern:

  User Query: “{query}”  
  Assistant (ask follow-ups):  

  """
  return callLLM(prompt)

def recommFinalQuery(query,answers):

  prompt = f"""
  You are an expert assistant that takes a user's initial query and their answers to follow-up questions, then creates a structured, enriched query for semantic search in a beauty product database.

  Format the final output as:
  Category: <product category>
  Description: <brief 1–2 line summary of what the user is looking for>
  Top Ingredients: <list of ingredients mentioned or inferred as desirable or avoidable>
  Tags: <skin concerns, preferences, skin type, seasonal needs, etc.>

  Examples:

  ### Example 1
  User Query: “serums”  
  Follow-up Answers:  
  - Skin concern: hydration  
  - Skin type: dry and flaky  
  - Preference: fragrance-free  

  Output:  
  Category: Serum  
  Description: Looking for a hydrating serum suitable for dry and flaky skin, preferably fragrance-free.  
  Top Ingredients: Hyaluronic acid, glycerin  
  Tags: dry skin, hydration, fragrance-free

  ---

  ### Example 2
  User Query: “something gentle for summer”  
  Follow-up Answers:  
  - Product category: SPF and moisturizers  
  - Skin concerns: acne-prone, sensitive to fragrance  
  - Ingredient to avoid: alcohol  

  Output:  
  Category: SPF, Moisturizer  
  Description: Needs a gentle, summer-friendly SPF and moisturizer for acne-prone, sensitive skin. Prefers fragrance-free and alcohol-free options.  
  Top Ingredients: Zinc oxide, niacinamide  
  Tags: summer, sensitive skin, acne-prone, fragrance-free, alcohol-free

  ---

  Now generate the structured query for this case:

  User Query: {query}  
  {answers}

  Output:
  """

  return callLLM(prompt)

def RAG(results,user_question):

  context_text = "\n\n".join(results["documents"][0])
  prompt = f"""
  You are an expert skincare consultant. Use ONLY the information provided under “Context” to answer the question below. 
  The answer to the question would exist in the Context and if not, maybe rethink the question and give the answer.

  Context:
  {context_text}

  Question:
  {user_question}

  Answer:
  """

  return callLLM(prompt)

def getProducts(query,catalog_collection):
    data = catalog_collection.query(
    query_texts=[query], 
   n_results=5 
    )
    product_list = data['metadatas'][0]

    # Sort by margin in descending order
    sorted_products = sorted(product_list, key=lambda x: x['margin'], reverse=True)

    # Create new list containing only Name, price, and margin
    result = [{'Name': p['Name'], 'price': p['price'], 'margin': p['margin']} for p in sorted_products]

    return result
