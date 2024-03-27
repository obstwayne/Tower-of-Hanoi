import tkinter as tk

class TowerOfHanoi:
    def __init__(self, root, num_discs=4):
        self.root = root
        self.num_discs = num_discs
        self.disks = [[i for i in range(num_discs, 0, -1)], [], []]
        self.selected_disk = None
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()
        self.draw_towers()
        self.draw_discs()
        self.canvas.bind("<Button-1>", self.select_disk)
        self.canvas.bind("<B1-Motion>", self.move_disk)
        self.canvas.bind("<ButtonRelease-1>", self.place_disk)

    def draw_towers(self):
        '''Рисуем стержни'''
        self.canvas.delete("tower")
        for i in range(3):
            x = 100 + i * 200
            self.canvas.create_rectangle(x-5, 50, x+5, 350, fill="black", tags="tower")

    def draw_discs(self):
        '''Рисуем диски'''
        self.canvas.delete("disc")
        for i, tower in enumerate(self.disks):
            x = 100 + i * 200
            for j, size in enumerate(tower):
                if size is not None:
                    y = 350 - (j * 20)
                    self.canvas.create_rectangle(x-size*10, y, x+size*10, y-20, fill="blue", tags="disc")


    def select_disk(self, event):
        '''Выбор диска'''
        x, y = event.x, event.y
        for i, tower in enumerate(self.disks):
            if not tower:
                continue
            # Если стержень пуст, идем дальше
            max_size = max(tower, default=0)
            #левая граница: левая граница стержня - размер самого большого диска * 10(отступ)
            #правая граница: правая граница стержня + размер самого большого диска * 10
            x_range = range(100 + i * 200 - max_size * 10, 100 + i * 200 + max_size * 10)
            #нижняя граница: нижняя граница - высота дисков * 20(отступ)
            #верхняя граница: 350
            y_range = range(350 - len(tower) * 20, 350)
            if x in x_range and y in y_range:
                self.selected_disk = tower[-1]
                # Удаляем выбранный диск из стека
                tower.pop()
                self.draw_discs()
                break


    def move_disk(self, event):
        '''Удаляем выбранный диск и отрисовываем на новых координатах'''
        if self.selected_disk is not None:
            x, y = event.x, event.y
            self.canvas.delete("selected_disk")
            self.canvas.create_rectangle(x-10, y, x+10, y-20, fill="red", tags="selected_disk")

    def place_disk(self, event):
        '''Можно ли поставить диск на новый стержень'''
        x, y = event.x, event.y
        target_tower = (x - 100) // 200
        if 0 <= target_tower < 3:
            #Выбранный стержень пустой? + (Диск выбран? * (Выбранный стержень доступен? + Выбранный диск < Верхнего диска на выбранном стержне))
            if not self.disks[target_tower] or (self.selected_disk is not None and (not self.disks[target_tower] or self.selected_disk < self.disks[target_tower][-1])):
                # Добавляем выбранный диск в стержень
                self.disks[target_tower].append(self.selected_disk)
            else:
                print("Нельзя положить диск на диск меньшего размера")
                # Возвращаем диск на исходный стержень
                self.disks[0].append(self.selected_disk)
        else:
            print("Нельзя положить диск вне башни")
            # Возвращаем диск на исходный стержень
            self.disks[0].append(self.selected_disk)
        self.selected_disk = None
        self.canvas.delete("selected_disk")
        self.draw_discs()
        if not self.disks[0] and not self.disks[1]:
            print("Победа!")


def main():
    root = tk.Tk()
    root.title("Ханойская башня")
    root.geometry("800x500")
    game = TowerOfHanoi(root)
    root.mainloop()

if __name__ == "__main__":
    main()
