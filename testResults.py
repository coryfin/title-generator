def test(story_words, story_titles):

    total_precision=0
    total_recall=0

    i=0
    for story_title in story_titles:

        gen_keywords = story_words[i]
        num_real_keywords = len(story_title)


        correct = 0

        for i in range(0,len(gen_keywords)):
            if gen_keywords[i] in set(num_real_keywords):
                correct += 1
        if len(gen_keywords)>0:
            total_precision += correct/float(len(gen_keywords))
            total_recall += correct/float(len(story_title))
            print('correct:', correct, 'out of', num_real_keywords)
        else:
            total_precision+=0
            total_recall+=0
            print('no tags predicted')

        i+=1


    avg_precision = round(total_precision/float(file.shape[0]), 2)
    avg_recall = round(total_recall/float(file.shape[0]), 2)

    avg_fmeasure = round(2*avg_precision*avg_recall/(avg_precision + avg_recall), 2)

    print("Precision", avg_precision, "Recall", avg_recall, "F-Measure", avg_fmeasure)

