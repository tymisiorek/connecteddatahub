# ──────────────────────────────────────────────────────────────────────────────
# Presentation-Ready: Average Board Size by Year (with public/private lines)
# ──────────────────────────────────────────────────────────────────────────────

# 1) Load libraries (suppress startup messages)
suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
})

# 2) Define file paths
data_dir    <- "C:/Projects/connecteddatahub/data/statistics"
input_file  <- file.path(data_dir, "regression_university_board_statistics.csv")
output_file <- "average_board_size_by_year.png"

# 3) Read data and rename Control column to lowercase
stats_df <- read_csv(input_file, show_col_types = FALSE)

# 4) Compute overall yearly average
avg_by_year <- stats_df %>%
  group_by(Year) %>%
  summarise(average_members = mean(total_members, na.rm = TRUE)) %>%
  arrange(Year)

# 5) Compute yearly average by control type (public vs private)
avg_by_year_control <- stats_df %>%
  filter(control %in% c('Public', 'Private')) %>%
  group_by(Year, control) %>%
  summarise(average_members = mean(total_members, na.rm = TRUE)) %>%
  arrange(control, Year)

# 6) Build the combined line plot
line_plot <- ggplot() +
  # overall average
  geom_line(
    data   = avg_by_year,
    aes(x   = Year, y = average_members),
    size   = 1,
    alpha  = 0.8,
    colour = "black"
  ) +
  geom_point(
    data   = avg_by_year,
    aes(x   = Year, y = average_members),
    size   = 3,
    alpha  = 0.8,
    colour = "black"
  ) +
  # public vs private lines
  geom_line(
    data   = avg_by_year_control,
    aes(x   = Year, y = average_members, colour = control),
    size   = 1,
    alpha  = 0.8
  ) +
  geom_point(
    data   = avg_by_year_control,
    aes(x   = Year, y = average_members, colour = control),
    size   = 2,
    alpha  = 0.8
  ) +
  scale_colour_manual(
    name   = "control type",
    values = c('Public' = 'steelblue', 'Private' = 'salmon')
  ) +
  scale_x_continuous(breaks = avg_by_year$Year) +
  scale_y_continuous(limits = c(22, 28)) +
  labs(
    x = "Year",
    y = "Average Total Members"
  ) +
  theme_classic(base_size = 14) +
  theme(
    axis.title.x       = element_text(size = 22),
    axis.title.y       = element_text(size = 22),
    axis.text.x        = element_text(size = 12),
    axis.text.y        = element_text(size = 12),
    panel.grid.major.y = element_line(color = "grey90"),
    panel.grid.major.x = element_blank(),
    panel.grid.minor   = element_blank()
  )

# 7) Render to screen
print(line_plot)

# 8) Save high-res PNG for slides (same size as interlocks plot)
ggsave(
  filename = output_file,
  plot     = line_plot,
  path     = data_dir,
  width    = 10,
  height   = 6,
  units    = "in",
  dpi      = 300
)

