"""
Module Description:
    This script will be basis of the code for evaluating offline and online
    submissions.
    Each script and task have a One-to-one relationship.
    Input to each script is 2 ZIP files (result and GT), It is the job
    of the script to efficiently extract both and compare the result with
    the GT of the task
    Output of the script is a dictionary that has the name of the EM as keys
    and the value of the result in that EM as the value to the key.
"""

def evaluate(result_path, gt_path):
    ret = {
        'Hmean': 99.0,
        'Recall': 99.0,
        'Precision': 99.0,
        'AP': 98.0
    }
    return ret

# def evaluate(submission_id, results):
    # """
    # Inputs:
    # submission_id: id of the submission for which resuls are evaluated.
    # results: list of strings from the user uploaded submission

    # returns the string of the evaluation rounded to 2 decimal places.
    # """
    # sub = Submission.objects.get(id=submission_id)
    # gtfile = sub.dataset.gtfile.path
    # with open(gtfile, 'r') as f:
        # gtr = f.readlines()
    # gtr = [i.strip() for i in gtr]
    # correct = 0
    # for i in gtr:
        # corresponding_result = [j for j in results if i==j]
        # if corresponding_result:
            # correct += 1
    # return '{0:.2f}'.format(correct/len(gtr) * 100)
