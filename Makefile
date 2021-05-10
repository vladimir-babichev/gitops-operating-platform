ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
PROJECT_NAME := $(filter-out $@,$(MAKECMDGOALS))

.PHONY: deploy
deploy:
	# kubectl create namespace $(filter-out $@,$(MAKECMDGOALS)) --dry-run=client -o yaml | kubectl apply -f -
	helm upgrade -i \
		--create-namespace \
		-n $(filter-out $@,$(MAKECMDGOALS)) \
		$(filter-out $@,$(MAKECMDGOALS))-gitops \
		$(ROOT_DIR)/projects/$(filter-out $@,$(MAKECMDGOALS))

%:
	@:
