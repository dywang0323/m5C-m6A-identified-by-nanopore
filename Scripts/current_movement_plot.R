library(tidyverse)
library(cowplot)
require(magick)
library(extrafont)

# Figure 7A
df_nvrna = read.delim("/work/schroederrna/Current_density/hbec021420_vs_hbecpolya_GGACT1.txt", sep = "\t")

p_eef2_nvrna <- ggplot(df_nvrna, aes(x = event_mean, fill= state)) +
  theme_cowplot(font_size = 14, font_family = "ArialMT", line_size = 1)+
  geom_density(alpha= 0.5) +
  #facet_wrap(~ dataset,ncol=2) +
  theme(strip.background =element_rect(fill="white")) +
  scale_fill_manual(name="",values = c(Modified="#1f77b4", Unmodified="#ff7f0e"),labels=c("hbec021420", "hbecpolya")) +
  geom_segment(aes(x = 123.8, xend = 123.8, y = 0, yend = 0.15,linetype= "Pore Model"),color="black",size=1 ) +
  scale_linetype_manual(name="",values = c("Pore Model"=2)) +
  theme(legend.position="top")
save_plot("/work/schroederrna/Current_density/hbec021420_vs_hbecpolya.pdf", p_eef2_nvrna, base_aspect_ratio = 1.5)
