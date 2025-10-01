main:
		make adobe
		make mozilla

adobe:
		poe adobe > data/adobe.json

mozilla:
		poe mozilla > data/mozilla.json

format:
		uvx ruff check --select I --fix
		uv format --preview-features format
