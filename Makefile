main:
		uv run main.py

adobe:
		poe adobe

mozilla:
		poe mozilla

format:
		poe lint
		# uvx ruff check --fix
		# uv format --preview-features format
