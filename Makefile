.PHONY: all zip linux windows run clean distclean mkdist

END=\033[0m
GREEN=\033[34m
NAME=game

all: linux windows zip

zip: mkdist
	@echo -e "$(GREEN)Updating zip...$(END)"
	@git ls-files | zip --filesync -r --names-stdin dist/$(NAME).zip

linux: mkdist
	@echo -e "$(GREEN)Building for linux...$(END)"
	PYTHONPATH=src poetry run pyinstaller --noconsole --add-data src/assets/:src/assets --onefile $(NAME).py

windows: mkdist
	@echo -e "$(GREEN)Building for windows...$(END)"
	WINEDEBUG=-all wine pyinstaller.exe --noconsole --add-data src\\assets\;src\\assets --onefile $(NAME).py

run:
	@poetry run python $(NAME).py

clean:
	rm -rf build
	rm -rf */*/__pycache__ __pycache__

distclean: clean
	rm -rf dist

mkdist:
	@mkdir -p dist
