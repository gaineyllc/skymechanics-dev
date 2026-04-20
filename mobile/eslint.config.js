/* eslint-disable */
/* eslint-disable react/react-in-jsx-scope */
/* eslint-disable react/jsx-uses-react */
/* eslint-disable react/jsx-uses-vars */
/** @type {import('eslint').Linter.Config} */
module.exports = {
  root: true,
  extends: '@react-native',
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint'],
  rules: {
    'react/react-in-jsx-scope': 'off',
    'react/jsx-uses-react': 'off',
    'react/jsx-uses-vars': 'off',
  },
};
