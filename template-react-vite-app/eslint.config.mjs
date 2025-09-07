import eslintJs from '@eslint/js';
import globals from 'globals';
import prettier from 'eslint-plugin-prettier';
import react from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';
import reactRedux from 'eslint-plugin-react-redux';
import reactRefresh from 'eslint-plugin-react-refresh';
import eslintPluginPrettierRecommended from 'eslint-plugin-prettier/recommended';

import tseslint from 'typescript-eslint';

export default tseslint.config(
  { ignores: ['dist'] },
  {
    extends: [eslintJs.configs.recommended, ...tseslint.configs.recommended],
    files: ['**/*.{js,jsx,mjs,cjs,ts,tsx}'],
    languageOptions: {
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
        globals: {
          ...globals.browser,
          ...globals.node,
        },
      },
    },
    plugins: {
      react,
      'react-hooks': reactHooks,
      'react-redux': reactRedux,
      'react-refresh': reactRefresh,
      prettier,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      ...reactRedux.configs.recommended.rules,
      'react-refresh/only-export-components': [
        'warn',
        { allowConstantExport: true },
      ],
      'semi': 'error',
      'prefer-const': 'error',
      'no-nested-ternary': 'error',
      'prettier/prettier': 'warn',
    },
  },
  {
    settings: {
      react: {
        createClass: 'createReactClass', // Regex for Component Factory to use,
        // default to "createReactClass"
        pragma: 'React', // Pragma to use, default to "React"
        fragment: 'Fragment', // Fragment to use (may be a property of <pragma>), default to "Fragment"
        version: 'detect', // React version. "detect" automatically picks the version you have installed.
        // You can also use `16.0`, `16.3`, etc, if you want to override the detected value.
        // Defaults to the "defaultVersion" setting and warns if missing, and to "detect" in the future
        defaultVersion: '', // Default React version to use when the version you have installed cannot be detected.
        // If not provided, defaults to the latest React version.
        flowVersion: '0.53', // Flow version
      },
      propWrapperFunctions: [
        // The names of any function used to wrap propTypes, e.g. `forbidExtraProps`. If this isn't set, any propTypes wrapped in a function will be skipped.
        'forbidExtraProps',
        { property: 'freeze', object: 'Object' },
        { property: 'myFavoriteWrapper' },
        // for rules that check exact prop wrappers
        { property: 'forbidExtraProps', exact: true },
      ],
      componentWrapperFunctions: [
        // The name of any function used to wrap components, e.g. Mobx `observer` function. If this isn't set, components wrapped by these functions will be skipped.
        'observer', // `property`
        { property: 'styled' }, // `object` is optional
        { property: 'observer', object: 'Mobx' },
        { property: 'observer', object: '<pragma>' }, // sets `object` to whatever value `settings.react.pragma` is set to
      ],
      formComponents: [
        // Components used as alternatives to <form> for forms, eg. <Form endpoint={ url } />
        'CustomForm',
        { name: 'SimpleForm', formAttribute: 'endpoint' },
        { name: 'Form', formAttribute: ['registerEndpoint', 'loginEndpoint'] }, // allows specifying multiple properties if necessary
      ],
      linkComponents: [
        // Components used as alternatives to <a> for linking, eg. <Link to={ url } />
        'Hyperlink',
        { name: 'MyLink', linkAttribute: 'to' },
        { name: 'Link', linkAttribute: ['to', 'href'] }, // allows specifying multiple properties if necessary
      ],
    },
  },
  react.configs.flat['jsx-runtime'],
  eslintPluginPrettierRecommended,
);
