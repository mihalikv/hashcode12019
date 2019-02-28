from random import randint

HORIZONTAL = 'H'
VERTICAL = 'V'


class Image(object):
    id = None
    tags = None
    orientation = HORIZONTAL

    def __init__(self, id, tags, orientation) -> None:
        super().__init__()
        self.id = id
        self.tags = set(tags)
        self.orientation = orientation

    def __str__(self) -> str:
        return self.id


class SlideShow(object):
    images = []

    def add_image(self, image, image2=None):
        if image and image2:
            self.images.append([image, image2])
        else:
            self.images.append(image)

    def get_transition_score(self, image1, image2):
        image1_tags = None
        image2_tags = None

        if type(image1) is list:
            image1_tags = image1[0].tags.union(image1[1].tags)
        else:
            image1_tags = image1.tags
        if type(image2) is list:
            image2_tags = image2[0].tags.union(image2[1].tags)
        else:
            image2_tags = image2.tags
        common = len(image1_tags.intersection(image2_tags))
        first = len(image1_tags - image2_tags)
        second = len(image2_tags - image1_tags)
        return min(common, first, second)

    def compute_score(self):
        result = 0
        for i in range(0, len(self.images), 2):
            if (i + 1) >= len(self.images):
                break
            result += self.get_transition_score(self.images[i], self.images[i + 1])
        return result

    def get_output(self):
        lines = list()
        lines.append('{}\n'.format(len(self.images)))
        for image in self.images:
            if type(image) is list:
                lines.append('{} {}\n'.format(image[0].id, image[1].id))
            else:
                lines.append('{}\n'.format(image.id))
        return lines

    def flush_images(self):
        self.images = []


def main():
    input_name = 'c_memorable_moments'
    slide_show = SlideShow()
    input_images = []
    vertical_indexes = []
    horizontal_indexes = []
    all_indexes = []
    with open('{}.txt'.format(input_name), 'r') as infile:
        lines = [x.strip() for x in infile.readlines()]
        num_of_images = int(lines.pop(0))
        for index, line in enumerate(lines):
            data = line.split(' ')
            orientation = line[0]
            tags = data[2]
            if len(tags) > 1:
                if orientation == HORIZONTAL:
                    horizontal_indexes.append(index)
                else:
                    vertical_indexes.append(index)
                all_indexes.append(index)
                input_images.append(Image(index, tags, orientation))

    # all_indexes = [0,1,2,3]
    # horizontal_indexes = [0,3]
    # vertical_indexes = [1,2]
    # input_iamges = [iamge, image, iamge, image]

    while len(all_indexes) > 0:
        index_of_image_index = randint(0, len(all_indexes) - 1)

        index_of_first_image = all_indexes[index_of_image_index]

        first_image_of_slide = input_images[index_of_first_image]
        if first_image_of_slide.orientation == VERTICAL:
            vertical_indexes.remove(index_of_first_image)
            if len(vertical_indexes) == 0:
                all_indexes.pop(index_of_image_index)
                continue
            index_of_image_index_vertical = randint(0, len(vertical_indexes) - 1)

            second_image_of_slide = input_images[vertical_indexes[index_of_image_index_vertical]]

            slide_show.add_image(first_image_of_slide, second_image_of_slide)

            all_indexes.remove(vertical_indexes[index_of_image_index_vertical])
            vertical_indexes.pop(index_of_image_index_vertical)
        else:
            horizontal_indexes.remove(index_of_first_image)
            slide_show.add_image(first_image_of_slide)
        all_indexes.pop(index_of_image_index)

    print(slide_show.compute_score())

    with open('{}.out'.format(input_name), 'w') as f:
        f.writelines(slide_show.get_output())


if __name__ == "__main__":
    main()
