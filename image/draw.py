from PIL import Image
import sys
import os

PATCH_NUM = 5
FEATURE = 7

HEIGHT = PATCH_NUM
WIDTH = FEATURE


def draw_7tuple(feature_list):
    PATCH_NUM = 5
    FEATURE = 7
    HEIGHT = PATCH_NUM
    WIDTH = FEATURE
    img = Image.new("RGB", (WIDTH, HEIGHT), "black")
    pixels = img.load()
    # print(pixels)
    # patch_number = int(raw_input("Number of patch to generate image: "))
    # from 0 ~ patch number
    counter = 0
    while len(feature_list) >= HEIGHT:
        # print(len(feature_list))
        for i in range(HEIGHT):
            # print("\n############Patch%d############")
            # print(feature_list[0])    

            # 3. packet count ratio
            MAXIMUN_THRESHOLD = 0.2
            unit = MAXIMUN_THRESHOLD / float(256)
            r = float(feature_list[i][2]) / unit
            pixels[0, i] = (int(r), 0, 0)
            
            # 24. PPf_all
            MAXIMUN_THRESHOLD = 1
            unit = MAXIMUN_THRESHOLD / float(256)
            g = float(feature_list[i][23]) / unit
            pixels[1, i] = (0, int(g), 0)
            # 25. PPf_interval
            MAXIMUN_THRESHOLD = 1
            unit = MAXIMUN_THRESHOLD / float(256)
            g = float(feature_list[i][24]) / unit
            pixels[2, i] = (0, int(g), 0)
            # 26. PPf_ratio
            MAXIMUN_THRESHOLD = 10
            unit = MAXIMUN_THRESHOLD / float(256)
            g = float(feature_list[i][25]) / unit
            pixels[3, i] = (0, int(g), 0)

            # 28. Entropy_all
            MAXIMUN_THRESHOLD = 5.5
            unit = MAXIMUN_THRESHOLD / float(256)
            b = float(feature_list[i][27]) / unit
            pixels[4, i] = (0, 0, int(b))
            # 29. Entropy_interval
            MAXIMUN_THRESHOLD = 5
            unit = MAXIMUN_THRESHOLD / float(256)
            b = float(feature_list[i][28]) / unit
            pixels[5, i] = (0, 0, int(b))
            # 30. Entropy_ratio
            MAXIMUN_THRESHOLD = 4
            unit = MAXIMUN_THRESHOLD / float(256)
            b = float(feature_list[i][29]) / unit
            pixels[6, i] = (0, 0, int(b))


            # print(pixels[6, i])
        
        feature_list = feature_list[5:]

        # APf = int(raw_input("APf: "))
        # ABf = int(raw_input("ABf: "))
        # ADf = int(raw_input("ADf: "))
        # GSf = int(raw_input("GSf: "))
        # GDP = int(raw_input("GDP: "))
        
        # Maximun PPf is 1, ratio of two-way flow & one-way flow
        # PPf = int(raw_input("PPf: "))

        # upper_bound = (HEIGHT / patch_number) * i
        # if i != patch_number-1:
        #     lower_bound = (HEIGHT / patch_number) * (i+1)
        # else:
        #     lower_bound = HEIGHT

        # # from 0 to feature
        # for j in range(FEATURE):
        #     # from upper bound to lower bound
        #     for k in range(upper_bound, lower_bound):
        #         left_bound = (WIDTH / FEATURE) * j
        #         if j != FEATURE - 1:
        #             right_bound = (WIDTH / FEATURE) * (j+1)
        #         else:
        #             right_bound = WIDTH
        #         # from left_bound to right bound
        #         for l in range(left_bound, right_bound):
        #             pixels[k, l] = (255, 0, 0)
                    # img.save("test.jpg")
        counter = counter + 1
        img.save("abnormal_pic/" + str(counter) + ".jpg")
    # pixels = list(img.getdata())


    # print(pixels[0, 0])

def main():
    if len(sys.argv) != 2:
        print "Usage : %s <data>" % sys.argv[0]
        sys.exit(1)

    feature_list = []
    filepath = sys.argv[1]
    filename_list = os.listdir(filepath)
    filename_list = sorted(filename_list)

    for i in range(len(filename_list)): 
        with open(filepath + "/" + filename_list[i]) as f:
            content = f.read().splitlines()
            feature_list.append(content)


    # global feature_list
    # print(feature_list[0])
        
    
    draw_7tuple(feature_list)


    #     if content[3] == 0:
    #         content[5] = 0
    #     else:
    #         content[5] = float(content[4]) - float(content[3]) /float(content[3])
    #     # all packet count
    #     # feature_list.append(content[0])
    #     # window's packet count
    #     # feature_list.append(content[1])
    #     # packet count ratio
    #     feature_list.append(content[2])
    #     # mean of all packte count
    #     feature_list.append(content[3])
    #     # mean of window's packet count
    #     feature_list.append(content[4])
    #     # packet mean ratio

    #     feature_list.append(content[5])
    #     # mean of all bytes count
    #     feature_list.append(content[6])
    #     # mean of window's bytes count
    #     feature_list.append(content[7])
    #     # bytes count ratio
    #     feature_list.append(content[8])
    #     # pair-flow
    #     # feature_list.append(content[9])
    #     # flow
    #     # feature_list.append(content[10])
    #     # window's pair-flow
    #     # feature_list.append(content[11])
    #     # window's flow
    #     # feature_list.append(content[12])
    #     # percentage of all pair-flow
    #     feature_list.append(content[13])
    #     # percentage of window's pair-flow
    #     feature_list.append(content[14])
    #     # pair-flow ratio
    #     feature_list.append(content[15])
    #     # entropy
    #     feature_list.append(content[16])
    #     # window's entropy
    #     feature_list.append(content[17])
    #     # entropy ratio
    #     feature_list.append(content[18])

    # print(feature_list)
    # # draw()

if __name__ == "__main__":
    main()
