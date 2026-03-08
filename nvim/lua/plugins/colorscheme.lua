return {
  {
    "folke/tokyonight.nvim",
    priority = 1000,
    config = function()
      require("tokyonight").setup({
        style = "night", -- night | storm | moon | day
        transparent = false,
        terminal_colors = true,
      })
    end,
  },

  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "tokyonight",
    },
  },
}
