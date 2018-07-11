# def title_screen():
#     pygame.mixer.music.load('happy.mp3')
#     pygame.mixer.music.set_volume(0.2)
#     pygame.mixer.music.play(-1)
#     background_image = pygame.image.load('frozen-lake.png').convert()

#     start_game = False

#     while not start_game:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 start_game = True
#                 done = True
        
#         screen.blit(background_image, [0, 0])
        
#         pygame.display.update()
#         clock.tick(60)
#     pygame.quit()