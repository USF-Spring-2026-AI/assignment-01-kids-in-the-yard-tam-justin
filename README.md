# AI Assignment 01 - Kids in the Yard

## AI Comparison Questions

### 1. Which tool(s) did you use?

I used Google Gemini for this.

### 2. If you used an LLM, what was your prompt to the LLM?

The initial prompt I gave to the LLM was this (including the assignment pdf as an attachment): Generate me a family tree program based on the information given in the implementation and design section of this pdf. Use an object-oriented approach. After you've done that. Add additional functionality to search the tree for a Person based on their name.

The LLM gave me decent results from this first prompt and understood the requirements to implement the family tree. I then uploaded all of the CSV files so that it could implement the logic and data retrieval methods needed to calculate attribute values of a Person object.

Then, I continuously iterated, pointing out mistakes the LLM made, such as misunderstanding the determinations for the last_name attribute and not evenly distributing the children amongst the eldest parent’s birth year + 25 & + 45. It also initially hard-coded the first two people based on the example given in the spec. I iterated until I cleared any logical issues that I saw in the code.

### 3. What differences are there between your implementation and the LLM?

My implementation and the LLM’s implementation differed in a few ways. The LLM read the CSV files in a much more organized manner, creating dictionaries that represented the relationship between probabilities, life_expectancies, and other rates with attributes wherever applicable. This made it so it didn’t have to do much lookup on DataFrames when calculating attributes. The LLM left all of the logic for generating children in the generate_tree() method, compared to my implementation having a separate method. The LLM also uses BFS to traverse the tree and collect all of the people in the tree for lookup on duplicate names, the total number of people in the tree, the total number of people by decade, and search.

### 4. What changes would you make to your implementation in general based on suggestions from the LLM?

Currently, the LLM suggests a few things to change in my implementation. One of the suggestions the LLM gave was that when I read the files in, I should cache the data into dictionaries so that I’m not performing a lookup each time I generate a new person. I think this is smart because it helps improve execution speed from O(n) to O(1). 

### 5. What changes would you refuse to make?

The LLM suggests that I change the way that I handle the statistics about the tree. Currently, I’m using variables and dictionaries to store information about the tree, incrementing values when generating new people. The LLM suggests that I remove the static state and instead use BFS to traverse the tree for each query the user has. I don’t think this is a smart thing to do, as traversing the tree for simple statistics is inefficient. If the tree had other functionality, perhaps changing a person’s name or something that required me to get to the actual Person object, I would implement BFS for that specifically.
