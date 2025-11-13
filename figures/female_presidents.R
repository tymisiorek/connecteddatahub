# ──────────────────────────────────────────────────────────────────────────────
# Presentation-Ready: Institutions with Female Presidents (All Years, PrimarySample)
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
output_file <- "institutions_female_president_primarysample.png"

# 3) Read and prepare data (filter to PrimarySample == TRUE)
stats_df <- read_csv(input_file, show_col_types = FALSE)
df_all   <- stats_df %>% 
  filter(PrimarySample == TRUE) %>% 
  mutate(female_president = factor(female_president, levels = c(FALSE, TRUE)))

# 3b) Count presidents and print to console
pres_counts <- df_all %>% count(female_president)
male_count   <- pres_counts %>% filter(female_president == FALSE) %>% pull(n)
female_count <- pres_counts %>% filter(female_president == TRUE)  %>% pull(n)

cat("Number of institutions with male president:  ", male_count,   "\n")
cat("Number of institutions with female president:", female_count, "\n")

# 4) Build the bar chart
bar_plot <- ggplot(df_all, aes(x = female_president)) +
  geom_bar(
    fill  = "#2C3E50",    # professional dark blue-grey
    color = "white",      # crisp white borders
    width = 0.6
  ) +
  scale_x_discrete(
    labels = c("FALSE" = "Man", "TRUE" = "Woman")
  ) +
  labs(
    x     = "President Gender",
    y     = "Number of Institutions"
  ) +
  theme_minimal(base_size = 14) +
  theme(
    plot.title         = element_text(face = "bold", size = 16),
    axis.title.x       = element_text(size = 22, face = "bold"),
    axis.title.y       = element_text(size = 22, face = "bold"),
    axis.text.x        = element_text(size = 12),
    axis.text.y        = element_text(size = 12),
    panel.grid.major.y = element_line(color = "grey80", linetype = "dashed"),
    panel.grid.major.x = element_blank(),
    panel.grid.minor   = element_blank(),
    axis.ticks         = element_blank()
  )

# 5) Render to screen
print(bar_plot)

# 6) Save high-res PNG for slides
ggsave(
  filename = output_file,
  plot     = bar_plot,
  path     = data_dir,
  width    = 6,
  height   = 4,
  units    = "in",
  dpi      = 300
)
