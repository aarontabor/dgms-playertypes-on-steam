library('ggplot2')
library('reshape2')
library('plyr')

new_theme = theme_bw(base_size = 16) +
  theme(panel.grid.major = element_line(size=.5, color="#ffffff"),
        panel.grid.minor.x = element_line(size=.5, color="#ffffff"),
        panel.grid.minor.y = element_line(size=.5, color="#ffffff"),
        #axis.text.x=element_blank(),
        axis.text.x = element_text(angle = 90, hjust = 1),
        axis.ticks.x=element_blank(),
        axis.line = element_line(size=.7, color="#ffffff"),
        panel.border = element_rect(fill=NA, color="#ffffff"),
        plot.margin=unit(c(2,2,2,2),"mm"),
        legend.position="bottom")


######################################################################################################################

df = read.csv('dataset.csv')

df <- rename(df, c("dgms_habit"="habit", 
             "dgms_moral"="moral",
             "dgms_agency"="agency",
             "dgms_escapism"="escapism",
             "dgms_narrative"="narrative",
             "dgms_pastime"="pastime",
             "dgms_performance"="performance",
             "dgms_social"="social"))

df_long = melt(df, 
               measure.vars=c('habit', 'moral', 'agency', 'narrative', 'escapism', 'pastime', 'performance', 'social'), 
               variable.name='dgms_category', 
               value.name='score')

ggplot(df_long, aes(x=dgms_category, y=score)) +
  geom_boxplot() +
  new_theme +
  guides(fill=guide_legend(title=NULL))
         
         
ggsave("dgms-distribution.png", width=18, height=10, units="cm", type="cairo-png")


##############################################################################################################################


df = read.csv('dataset.csv')

df <- rename(df, c("enjoy_action"="action", 
                   "enjoy_adventure" = "adventure",
                   "enjoy_casual" = "casual",
                   "enjoy_fps" = "fps",
                   "enjoy_mmorpg" = "mmorpg",
                   "enjoy_moba" = "moba",
                   "enjoy_platformer" = "platformer",
                   "enjoy_puzzle" = "puzzle",
                   "enjoy_rpg" = "rpg",
                   "enjoy_simulation" = "simulation",
                   "enjoy_sports" = "sports",
                   "enjoy_strategy" = "strategy"))

#df$action <- factor(df$action)
#df$adventure <- factor(df$adventure)
#df$casual <- factor(df$casual)
#df$fps <- factor(df$fps)
#df$mmorpg <- factor(df$mmorpg)
#df$moba <- factor(df$moba)
#df$platformer <- factor(df$platformer)
#df$puzzle <- factor(df$puzzle)
#df$rpg <- factor(df$rpg)
#df$simulation <- factor(df$simulation)
#df$sports <- factor(df$sports)
#df$strategy <- factor(df$stragety)

df_long = melt(df, 
               measure.vars=c('action', 'adventure', 'casual', 'fps', 'mmorpg', 'moba', 'platformer', 'puzzle', 'rpg', 'simulation', 'sports', 'strategy'), 
               variable.name='enjoy_category', 
               value.name='enjoy_response')

df_summary = ddply(df_long, c('enjoy_category'), summarize,
                   percent = mean(enjoy_response))

p = ggplot(df_summary, aes(x=enjoy_category, y=percent)) +
  geom_bar(stat="identity", position="dodge") +
  xlab(label='Genre') +
  ylab(label='Percent of Participants') +
  new_theme +
  scale_y_continuous(limits=c(0.0, 1.0), breaks=c(0, 0.2, 0.4, 0.6, 0.8, 1.0)) +
  scale_fill_discrete("")
p

ggsave("selfReportedPreferences-distribution.png", width=18, height=10, units="cm", type="cairo-png")

################################################################################################################



df = read.csv('dataset.csv')

df <- rename(df, c("owned_action_normalized"="action", 
                   "owned_adventure_normalized" = "adventure",
                   "owned_casual_normalized" = "casual",
                   "owned_fps_normalized" = "fps",
                   "owned_mmorpg_normalized" = "mmorpg",
                   "owned_moba_normalized" = "moba",
                   "owned_platformer_normalized" = "platformer",
                   "owned_puzzle_normalized" = "puzzle",
                   "owned_rpg_normalized" = "rpg",
                   "owned_simulation_normalized" = "simulation",
                   "owned_sports_normalized" = "sports",
                   "owned_strategy_normalized" = "strategy"))

df_long = melt(df, 
               measure.vars=c('action', 'adventure', 'casual', 'fps', 'mmorpg', 'moba', 'platformer', 'puzzle', 'rpg', 'simulation', 'sports', 'strategy'), 
               variable.name='owned_category', 
               value.name='owned_normalized_count')



ggplot(df_long, aes(x=owned_category, y=owned_normalized_count)) +
  geom_boxplot() +
  new_theme +
  xlab(label='Genre') +
  ylab(label='Percent of Game Collection') +
  scale_y_continuous(limits=c(0.0, 1.0), breaks=c(0, 0.2, 0.4, 0.6, 0.8, 1.0)) +
  scale_fill_discrete("")

ggsave("gameCollection-distribution.png", width=18, height=10, units="cm", type="cairo-png")

################################################################################################################


df = read.csv('dataset.csv')

df <- rename(df, c("playtime_action_normalized"="action", 
                   "playtime_adventure_normalized" = "adventure",
                   "playtime_casual_normalized" = "casual",
                   "playtime_fps_normalized" = "fps",
                   "playtime_mmorpg_normalized" = "mmorpg",
                   "playtime_moba_normalized" = "moba",
                   "playtime_platformer_normalized" = "platformer",
                   "playtime_puzzle_normalized" = "puzzle",
                   "playtime_rpg_normalized" = "rpg",
                   "playtime_simulation_normalized" = "simulation",
                   "playtime_sports_normalized" = "sports",
                   "playtime_strategy_normalized" = "strategy"))

df_long = melt(df, 
               measure.vars=c('action', 'adventure', 'casual', 'fps', 'mmorpg', 'moba', 'platformer', 'puzzle', 'rpg', 'simulation', 'sports', 'strategy'), 
               variable.name='playtime_category', 
               value.name='playtime_normalized_count')


ggplot(df_long, aes(x=playtime_category, y=playtime_normalized_count)) +
  geom_boxplot() +
  new_theme +
  xlab(label='Genre') +
  ylab(label='Percent of Hours Logged') +
  scale_y_continuous(limits=c(0.0, 1.0), breaks=c(0, 0.2, 0.4, 0.6, 0.8, 1.0)) +
  scale_fill_discrete("")

ggsave("hoursLogged-distribution.png", width=18, height=10, units="cm", type="cairo-png")

################################################################################################################


df = read.csv('dataset.csv')

df <- rename(df, c("achievements_action_normalized"="action", 
                   "achievements_adventure_normalized" = "adventure",
                   "achievements_casual_normalized" = "casual",
                   "achievements_fps_normalized" = "fps",
                   "achievements_mmorpg_normalized" = "mmorpg",
                   "achievements_moba_normalized" = "moba",
                   "achievements_platformer_normalized" = "platformer",
                   "achievements_puzzle_normalized" = "puzzle",
                   "achievements_rpg_normalized" = "rpg",
                   "achievements_simulation_normalized" = "simulation",
                   "achievements_sports_normalized" = "sports",
                   "achievements_strategy_normalized" = "strategy"))

df_long = melt(df, 
               measure.vars=c('action', 'adventure', 'casual', 'fps', 'mmorpg', 'moba', 'platformer', 'puzzle', 'rpg', 'simulation', 'sports', 'strategy'), 
               variable.name='achievement_category', 
               value.name='achievement_normalized_count')


ggplot(df_long, aes(x=achievement_category, y=achievement_normalized_count)) +
  geom_boxplot() +
  new_theme +
  xlab(label='Genre') +
  ylab(label='Percent of Achievements') +
  scale_y_continuous(limits=c(0.0, 1.0), breaks=c(0, 0.2, 0.4, 0.6, 0.8, 1.0)) +
  scale_fill_discrete("")

ggsave("achievements-distribution.png", width=18, height=10, units="cm", type="cairo-png")

################################################################################################################

