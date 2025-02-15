from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

import pandas as pd
import os

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

class AnalyzeSpreadsheetTool:
	name = "analyze_spreadsheet"
	description = "Tool to analyze data from an Excel file."

	def func(self):
		# Use an absolute path
		file_path = os.path.abspath('../data/financials_info.xlsx')
		data = pd.read_excel(file_path)

		# Example: Process the data
		# Perform analysis or extract data as needed
		print(data.head())  # Print the first few rows for demonstration

@CrewBase
class CofoAi():
	"""CofoAi crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def finance_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['finance_analyst'],
			verbose=True,
			tools=[AnalyzeSpreadsheetTool()]  # Use the tool class
		)

	@agent
	def finance_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['finance_manager'],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def analyze_excel_task(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_excel_task'],
		)

	@task
	def financial_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['financial_analysis_task'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the CofoAi crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
