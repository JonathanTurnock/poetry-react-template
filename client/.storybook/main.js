module.exports = {
  stories: ["../src/**/*.stories.jsx"],
  addons: [
    "@storybook/preset-create-react-app",
    "@storybook/addon-handler.ts",
    "@storybook/addon-links",
    "@storybook/addon-knobs/register",
  ],
};
