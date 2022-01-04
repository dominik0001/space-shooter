from arcade.experimental.crt_filter import CRTFilter
from pyglet.math import Vec2
from uuid import uuid4
from pyglet.math import Vec2
import arcade
import arcade.gui
import buttons
import math
import time
import random

# Background color must include an alpha component
MINIMAP_BACKGROUND_COLOR = arcade.get_four_byte_color(arcade.color.ALMOND)
MINIMAP_WIDTH = 256
MINIMAP_HEIGHT = 256
MAP_WIDTH = 22288
MAP_HEIGHT = 22288



class Globale:

    control_mode = "mouse"
    button_pressed = None

    game_music = arcade.load_sound("game_ambient.mp3")

    player_game_music = None
    music_play_game = False
    points = 0
    higscore = 0
    game_over = True


    @staticmethod
    def game():
        print("game")
        Globale.music_play_main_view = True
        Globale.player_game_music = Globale.game_music.play(loop=True)
        print("play game")

    @staticmethod
    def game_stop():
        print("game")
        if Globale.music_play_game:
            Globale.music_play_game = False
            if Globale.player_game_music:
                Globale.game_music.stop(Globale.player_game_music)
        print("stop game")

def load_animation(image):
    return arcade.load_texture(f"layer_{image}.png")


class Animationen:

    marker_1_animation = None
    len_marker_1_animation = None

    @staticmethod
    def load_animations():
        Animationen.marker_1_animation = []
        for i in range(0, 30):
            print(i)
            image = arcade.load_texture(f"munition_{i}.png")
            Animationen.marker_1_animation.append(image)
        Animationen.len_marker_1_animation = len(Animationen.marker_1_animation)


class Munition(arcade.Sprite):

    def higher(self, v1, v2):

        if v1 == v2:
            v2 += 1

        if v1 > v2:
            return int(v2), int(v1)
        return int(v1), int(v2)

    def new_pos(self, player):

        if random.randint(0, 1)==1:

            self.center_x = random.randrange(*self.higher(player.center_x-1001, player.center_x-400))
        else:
            self.center_x = random.randrange(*self.higher(player.center_x+400, player.center_x+1001))

        if random.randint(0, 1)==1:
            self.center_y = random.randrange(*self.higher(player.center_y-1001, player.center_y-400))
        else:
            self.center_y = random.randrange(*self.higher(player.center_y+400, player.center_y+1001))

    def __init__(self, high, player):

        super().__init__()
        
        self.new_pos(player)

        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y

        distance = math.sqrt(math.pow(dx, 2)+math.pow(dy, 2))

        if distance < 400:
            self.remove_from_sprite_lists()

        self.index = 0

        self.scale = 5

        self.set_hit_box([[1, 1], [1, -1], [-1, 1], [-1, -1]])

    def update_animation(self, delta_time: float = 1 / 60):
    
        if self.index > Animationen.len_marker_1_animation-1:
            self.index = 0

        self.texture = Animationen.marker_1_animation[self.index]

        self.index += 1


def load_texture(filename, l1=True, l2=True):

    return arcade.load_texture(filename, flipped_diagonally=l1, flipped_vertically=l2)


class PlayerCharacter(arcade.Sprite):

    def __init__(self):

        super().__init__()

        self.cur_texture = 0
        self.scale = 1
        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        self.idle_texture = load_texture("player.png", l1=False, l2=False)

        self.moving_textures = []
        for i in range(5):
            texture = load_texture(f"player.png", l1=False, l2=False)
            self.moving_textures.append(texture)

        self.speed = 0

    def update(self):

        angle_rad = math.radians(self.angle)

        self.angle += self.change_angle

        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)


    def update_animation(self, delta_time: float = 1 / 60):

        # Idle animation
        if self.speed == 0:
            self.texture = self.idle_texture
            return

        # Moving animation
        self.cur_texture += 1
        if self.cur_texture > 4 * 4:
            self.cur_texture = 0
        frame = self.cur_texture // 4
        self.texture = self.moving_textures[frame]


class Laser(arcade.Sprite):

    def __init__(self):

        super().__init__()

        self.cur_texture = 0
        self.scale = 1
        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        self.distace = 0

        self.moving_textures = []
        for i in range(6):
            texture = load_texture(f"laser_{i}.png", l1=False, l2=False)
            self.moving_textures.append(texture)

        self.speed = 30

    def update(self):

        angle_rad = math.radians(self.angle)

        self.angle += self.change_angle

        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)

    def update_animation(self, delta_time: float = 1 / 60):

        # Moving animation
        self.cur_texture += 1
        if self.cur_texture > 5 * 4:
            self.cur_texture = 0
        frame = self.cur_texture // 4
        self.texture = self.moving_textures[frame]


class Metreor(arcade.Sprite):

    def higher(self, v1, v2):

        if v1 == v2:
            v2 += 1

        if v1 > v2:
            return int(v2), int(v1)
        return int(v1), int(v2)

    def new_pos(self, player):

        if random.randint(0, 1)==1:

            self.center_x = random.randrange(*self.higher(player.center_x-1001, player.center_x-400))
        else:
            self.center_x = random.randrange(*self.higher(player.center_x+400, player.center_x+1001))

        if random.randint(0, 1)==1:
            self.center_y = random.randrange(*self.higher(player.center_y-1001, player.center_y-400))
        else:
            self.center_y = random.randrange(*self.higher(player.center_y+400, player.center_y+1001))

    def __init__(self, high, player, cool_down=0):

        super().__init__()

        self.cool_down = cool_down
        
        self.new_pos(player)

        dx = player.center_x - self.center_x
        dy = player.center_y - self.center_y

        distance = math.sqrt(math.pow(dx, 2)+math.pow(dy, 2))

        if distance < 400:
            self.remove_from_sprite_lists()

        self.angle = random.randint(0, 360)

        self.cur_texture = 0
        if random.randint(0, 25) == 0:
            self.scale = random.randint(10, 20)
        else:
            self.scale = random.randint(3, 8)

        if self.scale < 5:
            self.live_m = 1
        elif self.scale < 7:
            self.live_m = 2
        elif self.scale < 9:
            self.live_m = 4
        elif self.scale > 8:
            self.live_m = int(self.scale // 1.5)

        self.live = self.live_m

        self.points = [[-30, -30], [30, -30], [30, 30], [-30, 30]]
        
        self.m_type = random.randint(0, 2)
        l1 = bool(random.randint(0,1))
        l2 = bool(random.randint(0,1))
        self.texture = load_texture(f"metreor_{self.m_type}.png", l1=l1, l2=l2)

        self.speed = 5

    def update(self):

        if self.cool_down > 0:
            self.cool_down -= 1

        angle_rad = math.radians(self.angle)

        self.angle += self.change_angle

        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)

    def draw_me(self):

        if self.scale > 4:
            color = arcade.color.CASTLETON_GREEN
            if self.scale > 8:
                color = arcade.color.ARYLIDE_YELLOW
            width = 10 * (self.scale / 1.8)
            arcade.draw_rectangle_filled(center_x=self.center_x,
                                         center_y=self.center_y,
                                         width=width,
                                         height=20,
                                         color=arcade.color.ORCHID)

            balken = 0
            if self.live != 0:
                balken = (self.live * width) / self.live_m

            arcade.draw_rectangle_filled(center_x=self.center_x,
                                         center_y=self.center_y, 
                                         width=balken,
                                         height=20,
                                         color=color)


class Explosion(arcade.Sprite):

    def __init__(self, textures, scale, angle):

        super().__init__()

        self.textures = textures
        self.current_texture = 0
        self.scale = scale
        self.speed = 5
        self.angle = angle

    def update(self):

        angle_rad = math.radians(self.angle)

        self.angle += self.change_angle

        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)

    def update_animation(self):

        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()


class GameView(arcade.View):

    def __init__(self):

        super().__init__()
        self.setup()

        columns = 16
        count = 60
        sprite_width = 256
        sprite_height = 256
        file_name = "explosion.png"

        self.textures = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)


    def make_gui_paused(self):

        if self.manager:
            self.manager.disable()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.gui_box = arcade.gui.UIBoxLayout()

        self.text_label = arcade.gui.UITextArea(text="Game paused",  
                                                width=450,
                                                height=40,
                                                font_size=30,
                                                font_name="Kenney Future")

        self.gui_box.add(self.text_label.with_space_around(bottom=30, left=80))

        main_view_button = arcade.gui.UIFlatButton(text="Back to Menue", width=200)

        @main_view_button.event("on_click")
        def click(event):
            Globale.button_pressed = "main_view_button"

        self.gui_box.add(main_view_button.with_space_around(bottom=20))

        quit_button = QuitButton(text="Quit", width=200, font_size=50)
        self.gui_box.add(quit_button)

        if self.box:
            self.manager.children.clear()

        self.box = arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.gui_box)

        self.manager.add(self.box)


    def make_gui_skills(self):

        if self.manager:
            self.manager.disable()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.gui_box = None
        self.gui_box = arcade.gui.UIBoxLayout()

        self.text_label = arcade.gui.UITextArea(text="Improve skills",  
                                                width=450,
                                                height=40,
                                                font_size=30,
                                                font_name="Kenney Future")

        self.gui_box.add(self.text_label.with_space_around(bottom=50, left=80))

        self.text_label = arcade.gui.UITextArea(text=f"Skill points: {self.skill_points}",  
                                                width=450,
                                                height=40,
                                                font_size=20,
                                                font_name="Kenney Future")

        self.gui_box.add(self.text_label.with_space_around(bottom=50, left=80))

        button = arcade.gui.UIFlatButton(text=f"fill up hp\nCost: {self.hp_heal_cost}", width=400, height=50)
        button.on_click = self.health_heal
        self.gui_box.add(button.with_space_around(bottom=10, left=0))

        button = arcade.gui.UIFlatButton(text=f"Health Upgrade\ncurrent level: {self.hp_upgrade_level} | Cost: {self.hp_upgrade_cost}", width=400, height=100)
        button.on_click = self.health_upgrade
        self.gui_box.add(button.with_space_around(bottom=10, left=0))
        
        button = arcade.gui.UIFlatButton(text=f"fill up munition | Cost: {self.munition_fill_up_cost}", width=400, height=50)
        button.on_click = self.munitions_fill_up
        self.gui_box.add(button.with_space_around(bottom=10, left=0))

        button = arcade.gui.UIFlatButton(text=f"Munition Upgrade\ncurrent level: {self.munition_upgrade_level}\nCost: {self.munition_upgrade_cost}", width=400, height=100)
        button.on_click = self.munition_upgrade
        self.gui_box.add(button.with_space_around(bottom=160, left=0))

        if self.box:
            self.manager.children.clear()

        self.box = arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.gui_box)

        self.manager.add(self.box)

    def health_upgrade(self, event):
        
        if self.skill_points >= self.hp_upgrade_cost:
            self.hp_max += 5
            self.skill_points -= self.hp_upgrade_cost
            self.hp_upgrade_cost += 2
            self.hp_upgrade_level += 1
            self.button_succses.play()
        else:
            self.button_fail.play()
        self.make_gui_skills()

    def health_heal(self, event):
        
        if self.skill_points >= self.hp_heal_cost:
            self.hp = self.hp_max
            self.skill_points -= self.hp_heal_cost
            self.button_succses.play()
        else:
            self.button_fail.play()
        self.make_gui_skills()

    def munition_upgrade(self, event):
        
        if self.skill_points >= self.munition_upgrade_cost:
            self.munition_max += 5
            self.skill_points -= self.munition_upgrade_cost
            self.munition_upgrade_cost += 2
            self.munition_upgrade_level += 1
            self.button_succses.play()
        else:
            self.button_fail.play()
        self.make_gui_skills()

    def munitions_fill_up(self, event):
        
        if self.skill_points >= self.munition_fill_up_cost:
            self.munition_curr = self.munition_max
            self.skill_points -= self.munition_fill_up_cost
            self.button_succses.play()
        else:
            self.button_fail.play()
        self.make_gui_skills()

    def load_sound(self):

        self.explosion_1 = arcade.load_sound(":resources:sounds/explosion1.wav")
        self.explosion_2 = arcade.load_sound(":resources:sounds/explosion2.wav")
        self.lose_1 = arcade.load_sound(":resources:sounds/lose1.wav")
        self.lose_2 = arcade.load_sound(":resources:sounds/lose2.wav")
        self.lose_3 = arcade.load_sound(":resources:sounds/lose3.wav")
        self.shoot_1 = arcade.load_sound(":resources:sounds/laser1.wav")
        self.shoot_2 = arcade.load_sound(":resources:sounds/laser2.wav")
        self.shoot_3 = arcade.load_sound(":resources:sounds/laser3.wav")
        self.error = arcade.load_sound(":resources:sounds/error3.wav")
        self.munition_fail = arcade.load_sound(":resources:sounds/hurt1.wav")
        self.munition_succes = arcade.load_sound(":resources:sounds/coin2.wav")
        self.player_hit1 = arcade.load_sound(":resources:sounds/hit1.wav")
        self.player_hit2 = arcade.load_sound(":resources:sounds/hit2.wav")
        self.player_hit3 = arcade.load_sound(":resources:sounds/hit3.wav")
        self.upgrade1 = arcade.load_sound(":resources:sounds/upgrade1.wav")
        self.upgrade2 = arcade.load_sound(":resources:sounds/upgrade2.wav")
        self.upgrade3 = arcade.load_sound(":resources:sounds/upgrade3.wav")
        self.upgrade4 = arcade.load_sound(":resources:sounds/upgrade4.wav")
        self.upgrade5 = arcade.load_sound(":resources:sounds/upgrade5.wav")
        self.button_succses = arcade.load_sound("button_press_succes.mp3")
        self.button_fail = arcade.load_sound("button_press_fail.mp3")


    def setup(self):

        self.load_sound()

        self.width_d, self.height_d = self.window.get_size()

        self.manager = None

        self.player = PlayerCharacter()
        self.player.center_x = 800
        self.player.center_y = 100
        self.player_move = False
        self.player_delta_angle = 0

        self.box = None

        self.player_speed = 10
        self.player_speed_upgrade_cost = 4
        self.player_speed_upgrade_level = 1


        self.hp = 10
        self.hp_max = self.hp
        self.hp_heal_cost = 3
        self.hp_upgrade_cost = 4
        self.hp_upgrade_level = 1


        self.munition_max = 10
        self.munition_curr = self.munition_max
        self.munition_fill_up_cost = 1
        self.munition_upgrade_cost = 4
        self.munition_upgrade_level = 1
        
        
        self.xp = 0
        self.xp_c = False
        self.xp_add = 1
        self.xp_next_level = 10
        self.level = 1
        self.xp_add_upgrade_cost = 1
        self.xp_add_upgrade_level = 1
        self.skill_points = 0


        self.fire = False
        self.fire_rate = 1
        self.fire_rate_upgrade_cost = 8
        self.fire_rate_upgrade_level = 1


        self.points = 0

        self.laser_list = arcade.SpriteList()
        self.metreor_list = arcade.SpriteList()
        self.explosion_list = arcade.SpriteList()
        self.munition_list = arcade.SpriteList()

        self.mouse_x = 120
        self.mouse_y = 120

        self.c_now = buttons.controll_mode

        self.run = True
        self.game_over = False
        buttons.ok = False
        buttons.game_run = True
        buttons.controll_mode = "wasd"

        self.start_time = time.time()
        self.time_need = 0

        self.minimap_sprite_list = None
        self.minimap_texture = None
        self.minimap_sprite = None

        self.camera_sprites = arcade.Camera(self.width_d, self.height_d)
        self.camera_gui = arcade.Camera(self.width_d, self.height_d)

        self.crt_filter = CRTFilter(self.width_d, self.height_d,
                                    resolution_down_scale=2.8,
                                    hard_scan=-8.0,
                                    hard_pix=-3.0,
                                    display_warp = Vec2(1.0 / 32.0, 1.0 / 24.0),
                                    mask_dark=0.5,
                                    mask_light=1.5)

        size = (MINIMAP_WIDTH, MINIMAP_HEIGHT)
        self.minimap_texture = arcade.Texture.create_empty(str(uuid4()), size)
        self.minimap_sprite = arcade.Sprite(center_x=MINIMAP_WIDTH / 2,
                                            center_y=self.height_d - MINIMAP_HEIGHT / 2,
                                            texture=self.minimap_texture)

        self.minimap_sprite_list = arcade.SpriteList()
        self.minimap_sprite_list.append(self.minimap_sprite)

    def update_minimap(self):
        proj = 0, MAP_WIDTH, 0, MAP_HEIGHT
        self.minimap_sprite.draw_hit_box(arcade.color.YELLOW, 2)
        with self.minimap_sprite_list.atlas.render_into(self.minimap_texture, projection=proj) as fbo:
            fbo.clear(MINIMAP_BACKGROUND_COLOR)
            self.laser_list.draw()
            self.munition_list.draw()
            self.metreor_list.draw()
            self.explosion_list.draw()
            self.player.draw()


    def get_angle(self):
        
        dx = self.mouse_x - self.player.center_x
        dy = self.mouse_y - self.player.center_y

        winkelbogen = math.atan2(dy, dx)

        winkelgradmass = winkelbogen*180 / math.pi

        self.player.angle = winkelgradmass-90


    def get_distanze(self):

        dx = self.player.center_x - self.mouse_x
        dy = self.player.center_y - self.mouse_y

        distanze = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))

        return distanze

    def explosion(self, x, y, scale, angle):

        ex = Explosion(self.textures, scale, angle)
        ex.center_x = x
        ex.center_y = y
        self.explosion_list.append(ex)
        shake_direction = random.random() * 2 * math.pi
        shake_amplitude = 10
        shake_vector = (
                math.cos(shake_direction) * shake_amplitude,
                math.sin(shake_direction) * shake_amplitude
            )
        shake_speed = 2
        shake_damping = 0.9
        self.camera_sprites.shake(shake_vector,
                                      speed=shake_speed,
                                      damping=shake_damping)
        if random.random() > 0.7:
            self.explosion_1.play()
            return
        self.explosion_2.play()

    def center_camera_to_player(self):

        position = Vec2(self.player.center_x - self.width_d / 2,
                        self.player.center_y - self.height_d / 2)
        self.camera_sprites.move_to(position, 0.9)

    def on_update(self, delta_time: float):

        if self.xp_c:
            self.xp = self.xp_next_level + 100

        self.time_need = time.time() - self.start_time
        self.points = int(self.points)
        Globale.points = self.points

        if self.xp > self.xp_next_level:
            self.level += 1
            self.xp = 0
            f = self.level//10 if self.level//10 != 0 else 1
            self.xp_next_level += 10 * f
            self.skill_points += 1
            x = random.randint(0, 180)
            if x > 80:
                self.upgrade1.play()
            elif x > 120:
                self.upgrade2.play()
            elif x > 80:
                self.upgrade3.play()
            elif x > 40:
                self.upgrade4.play()
            else:
                self.upgrade5.play() 
                
        if not self.run:
            if buttons.ok:
                self.setup()
            elif Globale.button_pressed == "main_view_button":
                Globale.button_pressed = None
                view = LoseView()
                self.window.show_view(view)
            return

        if buttons.controll_mode == "mouse":

            self.get_angle()

            if self.get_distanze() < 40:
                self.player.speed = 0
            elif self.player_move:
                self.player.speed = self.player_speed

        else:

            self.player.angle += self.player_delta_angle

        self.player.update_animation(delta_time=delta_time)
        self.player.update()

        self.center_camera_to_player()

        if self.fire:

            self.player_fire()

        for laser in self.laser_list:

            laser.update_animation(delta_time=delta_time)
            laser.update()
            hit = arcade.check_for_collision_with_list(laser, self.metreor_list)
            for m in hit:
                m.live -= 1
                if m.live < 1:
                    self.explosion(laser.center_x, laser.center_y, m.scale, m.angle)
                    self.points += 10 * m.scale
                    Globale.points = self.points + (m.scale / 2) * 10
                    self.xp += self.xp_add + (m.scale / 2) * 2
                    m.remove_from_sprite_lists()
                else:
                    self.explosion(laser.center_x, laser.center_y, m.scale/2, m.angle)
                    self.xp += self.xp_add + int((m.scale / 2) * 1.01)
                laser.remove_from_sprite_lists()

        if len(self.laser_list)>1000:
            i = 0
            for laser in self.laser_list:
                i += 1
                if i > 500:
                    laser.remove_from_sprite_lists()

        if random.randint(0, 10) == 0 and len(self.metreor_list) < 1000:
            
            metreor = Metreor(self.height_d, self.player)
            self.metreor_list.append(metreor)

        if random.randint(0, 100) == 0:
            
            muni = Munition(self.height_d, self.player)
            self.munition_list.append(muni)

        for metreor in self.metreor_list:

            dx = self.player.center_x - metreor.center_x
            dy = self.player.center_y - metreor.center_y

            distance = math.sqrt(math.pow(dx, 2)+math.pow(dy, 2))

            if distance > 2000:
                metreor.remove_from_sprite_lists()


        if len(self.munition_list) > 30:
            i = 0
            for mun in self.munition_list:
                i += 1
                if i > 10:
                    mun.remove_from_sprite_lists()

        hit_list_muni = arcade.check_for_collision_with_list(self.player, self.munition_list)
        for muni in hit_list_muni:
            if self.munition_curr == self.munition_max:
                self.munition_fail.play()
            elif (self.munition_curr + 5) >= self.munition_max:
                self.munition_curr = self.munition_max
                self.munition_succes.play()
            else:
                self.munition_curr += (self.munition_max * 10) // 100
                self.munition_succes.play()
            muni.remove_from_sprite_lists()
        
        for metreor in self.metreor_list:

            metreor.update_animation(delta_time=delta_time)
            metreor.update()

        for muni in self.munition_list:
            muni.update_animation(delta_time)

        hit_list = arcade.check_for_collision_with_list(self.player, self.metreor_list)
        if len(hit_list) > 0:
            if hit_list[-1].scale > 8:
                self.hp = -1
            elif hit_list[-1].scale > 4:
                self.hp -= 1
            else:
                self.hp -= 1
            if self.hp < 1:
                x = random.randint(0, 30)
                if x > 20:
                    self.lose_1.play()
                elif x > 10:
                    self.lose_2.play()
                else:
                    self.lose_3.play()
                view = LoseView()
                self.window.show_view(view)
            else:
                x = random.randint(0, 30)
                if x > 20:
                    self.player_hit1.play()
                elif x > 10:
                    self.player_hit2.play()
                else:
                    self.player_hit3.play()
                view = LoseView()
                for metreor in hit_list:
                    self.explosion(metreor.center_x, metreor.center_y, metreor.scale, metreor.angle)
                    metreor.remove_from_sprite_lists()

        for metreor in self.metreor_list:

            if metreor.cool_down == 0:

                hit_list = []

                for sm in self.metreor_list:

                    sm_x = sm.center_x
                    sm_y = sm.center_y
                    
                    me_x = metreor.center_x
                    me_y = metreor.center_y

                    delta_x = me_x - sm_x
                    delta_y = me_y - sm_y

                    distance = math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2))
                
                    if distance < metreor.scale * 80 and not sm is metreor:
                        hit_list.append(sm)

                if len(hit_list) > 0:
                    self.explosion(metreor.center_x, metreor.center_y, metreor.scale, metreor.angle)
                    for m in hit_list:
                        for _ in range(random.randint(1, 3)):
                            if random.random() > 0.5: 
                                x_new = metreor.center_x + random.randint(20, 100)
                            else:
                                x_new = metreor.center_x - random.randint(20, 100)

                            if random.random() > 0.5: 
                                y_new = metreor.center_y + random.randint(20, 100)
                            else:
                                y_new = metreor.center_y - random.randint(20, 100)
                            size = metreor.scale // 2 if metreor.scale > 3 else None
                            if size == None:
                                break
                            mm = Metreor(self.height_d, self.player, cool_down=20)
                            mm.center_x = x_new
                            mm.center_y = y_new
                            mm.scale = size
                            self.metreor_list.append(mm)
                        m.remove_from_sprite_lists()
                    metreor.remove_from_sprite_lists()
            break

        for ex in self.explosion_list:

            ex.update_animation()
            ex.update()

        self.time_need = time.time() - self.start_time
        self.points = int(self.points)
        Globale.points = self.points

                

    def on_hide_view(self):
        
        if self.manager:
            self.manager.disable()

    def player_fire(self):
        for _ in range(self.fire_rate):
            if self.munition_curr > 0:
                self.munition_curr -= 1
                x = random.randint(0, 30)
                if x > 20:
                    self.shoot_1.play()
                elif x > 10:
                    self.shoot_2.play()
                else:
                    self.shoot_3.play()

                laser = Laser()
                laser.center_x = self.player.center_x
                laser.center_y = self.player.center_y
                laser.angle = self.player.angle
                self.laser_list.append(laser)
            else:
                self.error.play()

    def on_key_press(self, symbol: int, modifiers: int):
        
        if symbol == arcade.key.A:
            self.player_delta_angle = 4
        elif symbol == arcade.key.D:
            self.player_delta_angle = -4

        if symbol == arcade.key.F:
            self.fire = True

        if symbol == arcade.key.W:
            self.player.speed = self.player_speed
            self.player_move = True

        if symbol == arcade.key.ESCAPE and not self.game_over:
            self.make_gui_paused()
            self.run = False if self.run else True

        if symbol == arcade.key.E:
            self.make_gui_skills()
            self.run = False if self.run else True

        if symbol == arcade.key.X:
            self.xp += 100000000000000000000000000000000

        if symbol == arcade.key.C:
            self.xp_c = True



    def on_key_release(self, symbol: int, modifiers: int):

        if symbol == arcade.key.A:
            self.player_delta_angle = 0
        elif symbol == arcade.key.D:
            self.player_delta_angle = 0

        if symbol == arcade.key.SPACE:
            if self.run:
                self.player_fire()

        if symbol == arcade.key.F:
            self.fire = False

        if symbol == arcade.key.W:
            self.player.speed = 0
            self.player_move = False

        if symbol == arcade.key.C:
            self.xp_c = False

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):

        if buttons.controll_mode == "wasd":
            return

        if button == arcade.MOUSE_BUTTON_RIGHT:
            if self.run:
                self.player_fire()

        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player.speed = self.player_speed
            self.player_move = True

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        
        if scroll_y > 0:
            self.player.speed = self.player_speed
            self.player_move = True
        else:
            self.player.speed = 0
            self.player_move = False

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
    
        if buttons.controll_mode == "wasd":
            return

        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player.speed = 0
            self.player_move = False

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):

        self.mouse_x = x
        self.mouse_y = y


    def on_draw(self):

        self.camera_sprites.use()

        self.crt_filter.use()
        self.crt_filter.clear()
        self.munition_list.draw()
        if self.level > 20:
            i = 0
            for muni in self.munition_list:

                dx = self.player.center_x - muni.center_x
                dy = self.player.center_y - muni.center_y

                distance = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))

                if distance < 500*(self.level//10):
                    arcade.draw_line(self.player.center_x, self.player.center_y, muni.center_x, muni.center_y, arcade.color.BANANA_YELLOW, 5)
                    i += 1
                    if i > 5:
                        break
        self.metreor_list.draw()
        for m in self.metreor_list:
            m.draw_me()
        self.explosion_list.draw()
        self.laser_list.draw()
        self.player.draw()
        arcade.draw_text(f"X: {int(self.player.center_x)}, Y: {int(self.player.center_y)}, S: {len(self.laser_list)+1+len(self.metreor_list)} ----- Time: {int(self.time_need)}s", 10, 10, color=arcade.color.RED)
        if not self.run:
            self.manager.draw()

        self.camera_gui.use()


        arcade.draw_text(text=f"{int(self.time_need)} | {int(self.points)}",
                         start_x=self.width_d / 2 - len(f"{int(self.time_need)} | {self.points}")*10,
                         start_y=self.height_d - 50,
                         color=arcade.color.RED,
                         font_size=30)
        

        arcade.draw_text(text=f"{self.hp}",
                         start_x=self.width_d / 4,
                         start_y=60,
                         color=arcade.color.RED,
                         font_size=30)

        arcade.draw_text(text=f"{self.munition_curr}/{self.munition_max}",
                         start_x=self.width_d / 4 * 2,
                         start_y=60,
                         color=arcade.color.BANANA_YELLOW,
                         font_size=30)


        arcade.draw_text(text=f"{self.level} | {self.xp}/{self.xp_next_level}",
                         start_x=self.width_d / 4 * 3,
                         start_y=60,
                         color=arcade.color.SPANISH_BLUE,
                         font_size=30)

        width = 400

        x = self.width_d / 4 - 50

        arcade.draw_rectangle_filled(center_x=x,
                                     center_y=40, 
                                     width=width,
                                     height=30,
                                     color=arcade.color.ASH_GREY)

        balken = 0
        if self.hp != 0:
            balken = (self.hp * width) / self.hp_max

        arcade.draw_rectangle_filled(center_x=x,
                                     center_y=40, 
                                     width=balken,
                                     height=30,
                                     color=arcade.color.RED)

        width = 400

        x = self.width_d / 4 * 3 + 50

        arcade.draw_rectangle_filled(center_x=x,
                                     center_y=40, 
                                     width=width,
                                     height=30,
                                     color=arcade.color.ASH_GREY)
        balken = 0
        if self.xp != 0:
            balken = (self.xp * width) / self.xp_next_level

        arcade.draw_rectangle_filled(center_x=x,
                                     center_y=40, 
                                     width=balken,
                                     height=30,
                                     color=arcade.color.SPANISH_BLUE)

        width = 400

        x = self.width_d / 4 * 2

        arcade.draw_rectangle_filled(center_x=x,
                                     center_y=40, 
                                     width=width,
                                     height=30,
                                     color=arcade.color.ASH_GREY)

        balken = 0
        if self.munition_curr != 0:
            balken = (self.munition_curr * width) / self.munition_max

        arcade.draw_rectangle_filled(center_x=x,
                                     center_y=40, 
                                     width=balken,
                                     height=30,
                                     color=arcade.color.BANANA_YELLOW)

        self.window.use()
        self.window.clear()
        self.crt_filter.draw()


        #self.update_minimap()
        #self.minimap_sprite_list.draw()


class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()


class LoseView(arcade.View):

    def __init__(self):

        super().__init__()

        self.button_succses = arcade.load_sound("button_press_succes.mp3")
        
        if Globale.points > Globale.higscore:
            Globale.higscore = Globale.points
            text = f"!!! New Highscore !!!\nHighscore: {Globale.higscore}\nYour score: {Globale.points}"
        else:
            text = f"\nHighscore: {Globale.higscore}\nYour score: {Globale.points}"


        self.width_d, self.height_d = self.window.get_size()

        self.camera_gui = arcade.Camera(self.width_d, self.height_d)

        
        self.crt_filter = CRTFilter(self.width_d, self.height_d,
                                    resolution_down_scale=2.8,
                                    hard_scan=-8.0,
                                    hard_pix=-3.0,
                                    display_warp = Vec2(1.0 / 32.0, 1.0 / 24.0),
                                    mask_dark=0.5,
                                    mask_light=1.5)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()


        arcade.set_background_color(arcade.color.CHERRY)

        self.v_box = arcade.gui.UIBoxLayout()

        ui_text_label = arcade.gui.UITextArea(text="Game Over",
                                              width=600,
                                              height=80,
                                              font_size=50,
                                              font_name="Kenney Future")

        self.v_box.add(ui_text_label.with_space_around(bottom=40, left=self.width_d/2-650))            

        ui_text_label = arcade.gui.UITextArea(text=text,
                                              width=1200,
                                              height=200,
                                              font_size=40,
                                              font_name="Kenney Future")

        self.v_box.add(ui_text_label.with_space_around(bottom=40))

        start_button = arcade.gui.UIFlatButton(text="Retry", width=200)
        self.v_box.add(start_button.with_space_around(bottom=10))

        return_button = arcade.gui.UIFlatButton(text="Back", width=200, font_size=80)
        self.v_box.add(return_button.with_space_around(bottom=5))

        quit_button = QuitButton(text="Quit", width=200, font_size=50)
        self.v_box.add(quit_button)

        start_button.on_click = self.on_click_start

        @return_button.event("on_click")
        def on_click_settings(event):

            Globale.button_pressed = "main_view_button"

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_update(self, delta_time: float):
    
        if Globale.button_pressed == "main_view_button":

            Globale.button_pressed = None
            view = MainView()
            self.window.show_view(view)

    def on_click_start(self, event):
        self.button_succses.play()
        view = GameView()
        self.window.show_view(view)

    def on_hide_view(self):

        self.manager.disable()

    def on_draw(self):

        self.camera_gui.use()
    
        self.crt_filter.use()
        self.crt_filter.clear()

        self.manager.draw()

        self.window.use()
        self.window.clear()
        self.crt_filter.draw()


class SettingsView(arcade.View):

    def __init__(self):

        super().__init__()

        self.width_d, self.height_d = self.window.get_size()

        self.camera_gui = arcade.Camera(self.width_d, self.height_d)

        self.crt_filter = CRTFilter(self.width_d, self.height_d,
                                    resolution_down_scale=2.8,
                                    hard_scan=-8.0,
                                    hard_pix=-3.0,
                                    display_warp = Vec2(1.0 / 32.0, 1.0 / 24.0),
                                    mask_dark=0.5,
                                    mask_light=1.5)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        self.v_box = arcade.gui.UIBoxLayout()

        mode_button = arcade.gui.UIFlatButton(text=f"Mode: {Globale.control_mode}", width=200, font_size=30)
        self.v_box.add(mode_button.with_space_around(bottom=20))

        return_button = arcade.gui.UIFlatButton(text="return", width=200, font_size=30)
        self.v_box.add(return_button.with_space_around(bottom=20))

        quit_button = QuitButton(text="Quit", width=200, font_size=30)
        self.v_box.add(quit_button)

        mode_button.on_click = self.on_click_mode

        @return_button.event("on_click")
        def on_click_settings(event):
            
            Globale.button_pressed = "main_view_return_button"

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_update(self, delta_time):

        if Globale.button_pressed == "main_view_return_button":

            Globale.button_pressed = None
            view = MainView()
            self.window.show_view(view)

    def on_hide_view(self):

        self.manager.disable()

    def on_click_mode(self, event):

        Globale.control_mode = "mouse" if Globale.control_mode == "wasd" else "mouse"
        Globale.button_pressed = None
        view = SettingsView()
        self.window.show_view(view)

    def on_draw(self):

        self.camera_gui.use()
    
        self.crt_filter.use()
        self.crt_filter.clear()

        self.manager.draw()

        self.window.use()
        self.window.clear()
        self.crt_filter.draw()



class MainView(arcade.View):

    def __init__(self):

        super().__init__()

        Globale.game()

        self.width_d, self.height_d = self.window.get_size()

        self.camera_gui = arcade.Camera(self.width_d, self.height_d)

        
        self.crt_filter = CRTFilter(self.width_d, self.height_d,
                                    resolution_down_scale=2.8,
                                    hard_scan=-8.0,
                                    hard_pix=-3.0,
                                    display_warp = Vec2(1.0 / 32.0, 1.0 / 24.0),
                                    mask_dark=0.5,
                                    mask_light=1.5)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        self.v_box = arcade.gui.UIBoxLayout()

        ui_text_label = arcade.gui.UITextArea(text="   space sh00ter",
                                              width=650,
                                              height=250,
                                              font_size=80,
                                              font_name="Kenney Future")
        self.v_box.add(ui_text_label.with_space_around(bottom=30, left=45))

        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200, font_size=80)
        self.v_box.add(settings_button.with_space_around(bottom=20))

        quit_button = QuitButton(text="Quit", width=200, font_size=50)
        self.v_box.add(quit_button)

        start_button.on_click = self.on_click_start 

        @settings_button.event("on_click")
        def on_click_settings(event):

            Globale.button_pressed = "main_view_settings_button"

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_update(self, delta_time: float):
    
        if Globale.button_pressed == "main_view_settings_button":

            Globale.button_pressed = None
            view = SettingsView()
            self.window.show_view(view)

    def on_click_start(self, event):
        view = GameView()
        self.window.show_view(view)

    def on_hide_view(self):

        self.manager.disable()

    def on_draw(self):

        self.camera_gui.use()
    
        self.crt_filter.use()
        self.crt_filter.clear()

        self.manager.draw()

        self.window.use()
        self.window.clear()
        self.crt_filter.draw()



def main():
    Animationen.load_animations()
    window = arcade.Window(fullscreen=True)
    view = MainView()
    window.show_view(view)
    arcade.run()

if __name__ == "__main__":

    main()
