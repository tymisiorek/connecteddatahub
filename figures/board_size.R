# ──────────────────────────────────────────────────────────────────────────────
# Presentation-Ready: Interlocks in University Boards Over Time
# ──────────────────────────────────────────────────────────────────────────────

# 1) Load libraries (suppress startup messages)
suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
})

# 2) Define file paths
network_dir <- "C:/Users/tykun/OneDrive/Documents/SchoolDocs/VSCodeProjects/connectedData/board_analysis/final_scripts/network"
csv_file    <- file.path(network_dir, "network_interlocks", "yearly_interlock_stats.csv")
output_file <- "interlocks_over_time.png"

# 3) Read and prepare data
df_yearly <- read_csv(csv_file, show_col_types = FALSE)
df_unique <- df_yearly %>%
  distinct(Year, .keep_all = TRUE) %>%
  arrange(Year)

# 4) Build the line plot
line_plot <- ggplot(df_unique, aes(x = Year, y = Total_Interlocks)) +
  geom_line(color = "#000000", size = 1.5, alpha = 0.8) +
  geom_point(color = "#000000", size = 4, alpha = 0.8) +

  scale_x_continuous(breaks = df_unique$Year) +
  labs(x = "Year", y = "Number of Interlocks") +
  theme_minimal(base_size = 14) +
  theme(
    axis.title.x       = element_text(size = 22, face = "bold", margin = margin(t = 10)),
    axis.title.y       = element_text(size = 22, face = "bold", margin = margin(r = 10)),
    axis.text.x        = element_text(size = 12),
    axis.text.y        = element_text(size = 12),
    axis.line.x        = element_line(color = "black"),
    axis.line.y        = element_line(color = "black"),
    panel.grid.major.y = element_line(color = scales::alpha("grey80", 0.6), linetype = "dashed"),
    panel.grid.major.x = element_blank(),
    panel.grid.minor   = element_blank()
  )

# 5) Render to screen
print(line_plot)

# 6) Save high-res PNG for slides
ggsave(
  filename = output_file,
  plot     = line_plot,
  path     = network_dir,
  width    = 10,
  height   = 6,
  units    = "in",
  dpi      = 300
)
