Quick Guide: Creating Bioinformatics Analysis Questions

Goal and Overall Workflow
This guide summarizes how to convert a paper into a set of structured computational questions, each with:
Clean and well-documented data files,
A Jupyter notebook performing the intended analysis,
A final answer,
A scoring rubric,
A row in a centralized master spreadsheet.
Recommended structure:
your_paper/
question_1/
data_*.csv
question_1.ipynb
answer.txt
rubric.txt
Questions_Curated.xlsx
Step 1: Read the Paper Comprehensively
Before working on any questions, thoroughly read the entire paper to understand:
The biological context and research questions,
The experimental design and methodology,
The types of data collected and analyses performed,
The main findings and their biological interpretation.
This comprehensive understanding will help you effectively review, select, and modify questions in the next step.
Step 2: Review and Select Questions
Instead of designing questions from scratch:
Review the Questions_Curated.xlsx file associated with the paper,
Select 5 questions that are most relevant and feasible,
If some questions are impossible to perform with the available data, make necessary changes or create modified versions,
Ensure selected questions require actual computation (PCA, DE analysis, regression, clustering).
Common Question Types
Differential analysis (compare groups),
Association with phenotypes (with/without covariates),
Clustering/separation (PCA/UMAP),
Pathway enrichment,
Biomarker discovery/prediction.
Prepare and Document the Data
For each selected question:
Identify the required files for the question (RNA-seq, metabolites, metadata, etc.)
Download the data from the paper (could be downloading from GEO, supplementary or others)
Organized the files to each question’s folder and name files clearly: data_meta.csv, data_rnaseq.csv.
Step 3: Perform and Document the Analysis
Create a Jupyter notebook (question_X.ipynb) for each benchmark question that generally follows this workflow:

Start with the basics: State the biological question and hypothesis. Import libraries and load the data. Check the data dimensions and column names to verify everything loaded correctly. 

Preprocess the data: Filter samples, normalize values, and handle missing data. Save the cleaned data as an intermediate file so others can reproduce your work. 

Run the analysis: Perform the appropriate analyses to answer the biological question. Add notes when necessary to explain your approach. 

Generate and save results: Create necessary visualizations (scatter plots, heatmaps, boxplots) with clear labels and legends. Save all output files including data tables and figures in appropriate formats (CSV for tables, PNG and PDF for figures). 

Make sure it is reproducible: Add comments to clarify complex code. Ensure the notebook runs from start to finish without errors. 

Save everything: Put the notebook, all data files (raw and processed), results, and figures in the question folder with clear filenames.


Step 4: Write the Ground-Truth Answer
Based on your completed analysis, write a clear and comprehensive answer that directly addresses the biological question.

Best practices:
Be direct: Start with the main finding that answers the question (e.g., "Yes, rice-spikers separate from rice-eaters along PC1").
Be comprehensive: Address all parts of the question if it has multiple components.

This answer will serve as the ground-truth benchmark for evaluating AI-generated responses.

Step 5: Write the Scoring Rubric for Workflow
For each question, create a detailed scoring rubric that reflects the specific analysis performed. Rather than using a fixed number of criteria, generate step-by-step criteria based on the actual analysis workflow.
Rubric Components
Each rubric should include:
Question title and total points,
Overview of what the rubric evaluates,
Step-by-step criteria derived from your analysis workflow (data handling, preprocessing, methods, statistical validation, visualization, results, interpretation),
For each criterion: level descriptions (full credit, partial credit, zero credit),
Total sum: approximately 100 points.
Credit Levels
Full credit: correct method, complete analysis, proper interpretation,
Partial credit: correct method but incomplete or minor errors,
Zero credit: incorrect method or wrong dataset.
Step 5: Fill the Master Spreadsheet
Each row in Questions_Curated.xlsx corresponds to one question. Update or add rows with the following information:
Question Text: Full question (e.g., "Perform PCA..."),
Data Files: Required inputs (e.g., data_lipids.csv),
Answer: Analysis results (e.g., "Rice-spikers separate..."),
Rubric: Written rubric for workflow,
Difficulty: Level (e.g., Medium/Hard).
Best Practices
Do
Read the paper comprehensively before starting
Make questions specific and reproducible
Create rubrics that reflect the actual analysis steps
Add each finalized question to the master spreadsheet
Don't
Don't ask vague or underspecified questions
Don't leave code undocumented
Final Checklist
Paper has been read comprehensively,
5 questions selected or modified from Questions_Curated.xlsx,
Data files are clean and consistent,
Questions are concise and computational,
Notebooks run without errors,
Plots and results match the questions,
Rubrics are complete with step-by-step criteria based on the actual analysis,
Rows added to master spreadsheet.