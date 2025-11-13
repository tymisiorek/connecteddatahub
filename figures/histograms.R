# ──────────────────────────────────────────────────────────────────────────────
# Presentation‑Ready: Female Board Member Proportion Histogram
# ──────────────────────────────────────────────────────────────────────────────

# 1) Load libraries (suppress startup messages)
suppressPackageStartupMessages({
  library(readr)
  library(ggplot2)
  library(scales)      # for percent_format()
})

# 2) Define file paths
data_dir    <- "C:/Projects/connecteddatahub/data/statistics"
input_file  <- file.path(data_dir, "regression_university_board_statistics.csv")
output_dir  <- data_dir
output_file <- "female_board_proportion_histogram.png"

# 3) Read and prepare data
stats_df <- read_csv(input_file)
df2013   <- stats_df  # if you had a year column, you could filter here

# 4) Define bins for the histogram
bins <- seq(0, 0.7, by = 0.1)

# 5) Build the plot
hist_plot <- ggplot(df2013, aes(x = female_proportion)) +
  geom_histogram(
    breaks = bins,
    fill   = "#2C3E50",    # professional dark blue‑grey
    color  = "white",      # crisp white borders
    closed = "right"
  ) +
  scale_x_continuous(
    breaks = bins,
    limits = c(0, 0.8),
    labels = percent_format(accuracy = 1)  # “10%”, “20%”, etc.
  ) +
  scale_y_continuous(
    expand = expansion(mult = c(0, 0.02))
  ) +
  labs(
    x = "Women Board Member Proportion",
    y = "Number of Institutions"
  ) +
  theme_minimal(base_size = 14) +
  theme(
    plot.title         = element_text(face = "bold", size = 16),
    axis.title.x       = element_text(size = 22, face = "bold"),
    axis.title.y       = element_text(size = 22, face = "bold"),
    axis.text.x        = element_text(size = 12),
    axis.text.y        = element_text(size = 12),
    panel.grid.major.y = element_line(color = "grey80", linetype = "dashed"),
    panel.grid.major.x = element_line(color = "grey90"),
    panel.grid.minor   = element_blank(),
    axis.ticks         = element_blank()
  )

# 6) Render to screen
print(hist_plot)

# 7) Save high‑res PNG directly into the statistics folder
ggsave(
  filename = output_file,
  plot     = hist_plot,
  path     = output_dir,
  width    = 8,
  height   = 5,
  units    = "in",
  dpi      = 300
)
