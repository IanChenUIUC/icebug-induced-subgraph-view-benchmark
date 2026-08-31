library(tidyverse)
library(dplyr)
library(ggh4x)
library(scales)
library(ggstats)

data <- rbind(
  read.csv("ian-view/timing_view.csv") |> mutate(method = "Ian View"),
  read.csv("ian-view/timing_view_compact.csv") |> mutate(method = "Ian View (compact)"),
  read.csv("main/timing_gt.csv") |> mutate(method = "Graphtools"),
  read.csv("main/timing_gt_compact.csv") |> mutate(method = "Graphtools (compact)"),
  read.csv("main/timing_view.csv") |> mutate(method = "Main View")
)

data |> head()
data |> count(method)

data |>
  pivot_longer(cols = c("create_time", "decomp_time")) |>
  ggplot(aes(x = method, fill = name, y = value)) +
  facet_grid(cols = vars(factor(size))) +
  scale_x_discrete(name = "Method") +
  scale_y_continuous(
    name = "Runtime (s)",
    transform = pseudo_log_trans(base = 2),
    breaks = c(0, 1, 2, 4, 8, 16, 32)
  ) +
  geom_col() +
  theme_bw() +
  theme(
    axis.text.x = element_blank(),
    # axis.text.x = element_text(size = 12, angle = 30, hjust = 1),
    legend.position = "bottom"
  )
ggsave("timing.pdf")

data |>
  ggplot(aes(x = method, y = peak_delta_mb)) +
  facet_grid(cols = vars(factor(size))) +
  scale_x_discrete(name = "Method") +
  scale_y_continuous(
    name = "Memory (MB)",
    transform = pseudo_log_trans(base = 2),
    breaks = c(0, 1, 16, 256, 1024, 2048)
  ) +
  geom_col() +
  theme_bw() +
  theme(
    axis.text.x = element_blank(),
    # axis.text.x = element_text(size = 12, angle = 30, hjust = 1),
    legend.position = "bottom"
  )
ggsave("mem.pdf")
