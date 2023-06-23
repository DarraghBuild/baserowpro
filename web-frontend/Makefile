install-dependencies:
	yarn install

eslint:
	yarn run eslint || exit;

stylelint:
	yarn run stylelint || exit;

lint: eslint stylelint

lint-javascript: lint

jest:
	yarn test || exit;

test: jest

ci-test-javascript:
	yarn test-coverage || exit;
