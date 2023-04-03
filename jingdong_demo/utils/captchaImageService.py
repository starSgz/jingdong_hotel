import io

import gvcode
# from captcha.image import ImageCaptcha
import random

import base64
import uuid

from ..config  import redis_db


class OperateCaptcha:
    def generate_code(self, code_len=4):
        self.s, self.img = gvcode.generate()
        # code_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        # chars_len = len(code_chars) - 1
        # code = ''
        # for _ in range(code_len):
        #     index = random.randint(0, chars_len)
        #     code = code + code_chars[index]
        return self.img

    def generate_captcha_base64(self,code):
        # 将图片转换为BytesIO对象
        img_bytes_io = io.BytesIO()
        self.s.save(img_bytes_io, format='PNG')
        img_bytes_io.seek(0)

        # 将BytesIO对象转换为base64编码的字符串
        image_base64 = base64.b64encode(img_bytes_io.getvalue())
        image_base64_str = image_base64.decode('utf-8')

        return image_base64_str

    def generate_code_key(self):
        # 生成唯一标识
        code_key = str(uuid.uuid1()).replace('-','')
        return code_key


operate_captcha = OperateCaptcha()


def generate_captcha():
    '''
    :return: {'code_key': uuid, 'code_img': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKAAAAA8CAIAAABuCSZCAAAcs0lEQVR4nN196W9k15XfOXd5a22s4tJskr1I3S1pLI1GlrfxgrEzsT1JepAAQRIMgkGAfAiC+E/I3+Eg3wYOkjjBAJNBrFnsxJmxZXk8jjWWtVitXqQm2VyLZK1vvcvJh1cski0uxSpynOQHolH9qt69r+6559xzfufcW5jbFEbD9z7/reLF1378L0a85f82ILJotfPzf/sXjAMAG1wERAACIgDc/xwSWQAAsqme/+ozt//lq4b0r+ipJwKOKGDVyaLlztprDxfu3gqvV2XVvYynuexesnbWfnvryX9/kO/GgPvSLF4hcCIEAiIDzCIQABAwiU7gzU8/2/iH8/J5F+TFPtHFQHWy4sXHR0yM2ISsuuH16p1vvHpsKxeCQrr3/92bALD22sOir4sFWdq53yIEGooXABBEyXHLrl/irjIKWGwp7yvVz02qrSbVyrdxxWl6lcW6mHIu/KkmxOlaMaqA4dLkehhrrz0sXizcvXUZ7SPDqTtTvXs7B1cAgJgoB3Nfu1Ga9xGACEwC7V/sNn+ySmQtWsNNlscbP/1QLDqhW+HBOQZtRJyigmfeeLpWsAt5vovCwt1b4bXqnX/z6iWtAjKQMhBOePCtiUD4jj9VDW/W/Nt173bdv1MPb0815uar/jSKgZ7rRKfr0c5318yWxhhPaH5MDIT0zTej5c5Q0qPjdK04XsCqkxV/5+1sEgxXgctb4wEAARjgIQMNQompO3VJDtDgChPM+YTnvxw6gT/8qOrn+aMofyM1+UV6W0MVjFY6Q1GdC6drxTHW5lI8nb42kQYAKItTTNz5+iLQiUIAABzdbCIwAAYHHjOwMor7XHyWD6+QQziDtd+ai7odfT9X/RwAwFKSRy3Y8tMQQdBwOkyMwyqYdwY+74hDcaZv9LQGTz6hjoWOVfo/1puvr5j4wqa/TlS6Ea3/6aN4tZu3UqvsSLcRsMMfRAIi+qQBfuRTzOXOjNv40oJT8wqHjBBym+VZkqWJ1aP1NRqGKihrrmpn57XVsuoWf8e+e4yJnsTTMbHKm3HejG2kDl1GG+utzm5vpZ01Y5uZ8zZ7LGxstt940vrF9sof3es9bIE+pJUnA+Go6jFGdUt1hMrTn+S+dL3ALQfSysGdBvrL3Wi1S2qkvkbBUAUH0r1o1TrGsi3cvTW2fTaxaf7FCsSm/uXrLufMYwCo8ryfp/1cqfXI+fmGU/OcaQ8lgwm8RwA0iTbdPNnoy4qT76VWWw4j2E0kQILCRhMwh8l6WZY9YB8TGIL03Xp+JQo6kBAAGmVMnOtYkTIq10Vvky9hwxYe/8f3ihfHqtZ4Y/W0Bk/m6aCJVdqMm+/sbP9gM2tlVlsEoMyuf7Qabbd1N997a2vv7U3dzcHShN4jEBW2cxDTGsi7WbTWi9Z6qpORPUnWhMMVmIgJXlmsuRUfPy5gAB4K9gXBXUlQcCFgc2MzlW73o8ft8Z/8BJziLo09VseY6NNt+pmwlvIo2373yd5726avgMDkWdDOMU5NrlU3a/5otfdRK17rT7rYH5YuAFhKtuKVP3m4/F9/2fuorfvq+LsIkAZ2mgC4w7nLucOPONbDHqrI5iTMOdzhQASIVtn2L9Zb72ze/+bPLtaWnqJakzhGFx8HE4I12vaS3rtr6XaPLDnSESG6vsM4N5nJ9tLN7y+nW/HKH35Q3DI2rVFIqtBHsqQ6ab7a6T9qbf1wRXVPmOaIdqCNAACFsT5pPUWGfj2oPzfFxEDtbWayllr9b/cLC3GxhMwpqjW2Y3TBAiaEIgyxuUnWk3Q7Vv0cXDZ1+1l/ZoYhRwSdqHQ7af3vnfnfvjkZrYFAiJIJX/BAWks20za3Jtb5TpztxCZWJjcmM+aQW0eDPzp64YQOGEpfSN8R3oCDtgTWwtxXbgaXSch8HGNTQBfLuhEPJJaECIVq5zrWWz9YFSU3WKzIUhDOz+W7KutEOlY6ygmUOxOMS24jZhnEMcURgi3dqIVLVZvrzqO2SQwA6J5qvbUdLlbRob37u04gnJIjyy5zxFM6i0CFpT8RDFEwFKzwwhBAlp1gqbJw9xZz+KVLN80ASLoQXquMN1YXTKvygM/95lK20aPcmlilW9HKH77f+PTV+kvz01+a9RbE+v98ZI0la4mMrEhZ9UbxfI8BMniyClGfOZz7kvtS9TOzEZlUAYCOlYmVSTRqlnzU2n5/R1TcmS8s1e7MFLmjoUkuXOqTTDQBoWSi7okpj+0lRahtEs0cjo6Q1UtMPJC2qpfr3Yg/WeUv3JCzVTjOSzgFqpPJqnvBJlr40p8rLXz9drBQdmqeTXW2He38+MneOxtEJrxRnf3ikiy7KBgRTkQFkYXFJQpCoP1mjNVkQBf/pYER1mSbebLaj1e7ai+lAzLkFLEeAQr0Z0J/LgQ+GCuTmb13d3VBb10CrNYmU9lu3H5ne/m/vLf6syRtpjo5H0FU+GXf+/y3Lj4xIkqydLN245+9uPWD5fY726qT5t2s+cZqf6V79WvPVG5Nm9h0H+x5c6EI5JjqC0SuS4GPQQAsg0P0hcWjHCKBpUKWiB8T6Ch9M86Ey7nLGUetLTLQvdz2Eh2rw3znhYCU1b08a8f99S0bi53XN7KdBGVGP3iyWPHZXMjckeR1OMV08QJGhrLqck9c+e2bNs46H2jVV9muMbnd/v7Kla/eaHx6furVOe4K7l9Y73To32LQcRBFEYEtqjXo4LNHJPtxwR/zpYDIWMpN3s2cmmeVObAcFwQd5aqVtd/Zbv3NE62M6iubgE41Kug93Gn+iM995Y4zzQqC6EwMve6LF3AB5nJ32mt8biFZ2807FjjXfdV5tMtCNvdb152GJ0rOsdzCiLCZNrHSsTpKaBTLKyHgYXkCACHR8b2NZKfJACmbNWNAUJ3swhTXALTRdrVK8iTtbb7xYbwamV5mUkOIiIAIZEj1qf1+21/abdQWUT5Nth6Lgo78zL//e5clYACwytrMRJu5zjV3GHCr+lnrna18M1n4+q3SjTpMjd022sx23t9Nt2MieloHiQAG4rTKWGVNbsTAm4L9STB8RQBnjBgCIEqzz5yIqntRptn0lHmg8j/O9uR2mzbzfqp7igixmPvF4oJoFeVtne3luqccl50Z2x5OMV2WgItl4NF/eNfmxJA7NcekxuYmaxnIMPmT2Pv9kpwaM8ZAAJMaHecm09wVEiV1SG9p01NFKA4ACKQ6qY5U591tmxowBADIUARSBJK5YpDzIBjeciI4ky44dT/rprLqMYebwn4kSgTj1GhZbXVPqX6m15POa5u9vX6epErmFs3TUw0HrDlmkN5LzS0DdQR2tgYPo6lL1OBiGZAld+kfPdd9sNt+bxsAEND0TQs3S3FNkju2JgxNsKx5/kIl/0nW/GBV9dKC/AAA1U6j5c6T7zxIm7FJtT9fAgBg6F8p1z85n7fSrJXaXAPA6d48AXCXsZlANDwvCckQctS9vPXWVrhYhTEEbEl38r33dvb+et3uxXmktM6tQ0PfYJ8qp4PBQSCEoOtzNVI+5TAusWSnIF+e/VevePMlDAu+HgHAMK251vwErvgcQEDQyvSb0W62Ebe6uqsAB/leJFj7zgPVy3U/lxWXkAAIOcqqU31uunyngeygmVNB4PJwoezWAxQMOQMCHSsdK52oMWw1WUg2e7tvLPc/3Iu2+nk/M3DE80ci5MhLkoeSuaIgzTln7BXGZ47nzE/BZQn4gDq/Wk66ae9xm8wgBj3nE54ERCAwpHpp3O4qmxqeAxISA0IAtBZmv3wDJXNmAu4KxniRRkLBBlZa8hGVgQkmXC4cdsQrHPdb6H6W7cT5bmxSXUx6HBgRAiRAy0PhNXzv5lTl+WnStojYMWBYZlCBpwoTzsQlmmhZdRFQoaJeTL3EpmbfxT+N/h0JOUAPoIeQAQrNVAZWDKyaAQBGCKLiWoH+M7Xo4R53uHQ96fko2ccoDhzlWQjRskNGc4I5qvp56xebJrX7iRJAICRgDHlFippwa0H9U4uU263vP0aGAMQEd8q+rPgo2XlLhS5RwAVMnOs+pBsxATAmkI/gIZwFq615pMwDZckIlfO4RyRJa2BADMgSAgBSQW1wVwBCcLMUXC+hGFisI1zICCYFiWwx2EBkiAyenG8+FUQ6VirROtFD1w496ZEUJcdfKte/fNWd9khB/8OWSZTJDCAyX/jPVg4//+i4XAHnnTRe729895HqabLWnRUwIBYmMdNIyvZtq08t0mQdssurGgNrSyCIOJFmAACE4WxZt7NktYuS8VCIkDN50O9+fDxin9zX0ENGhqwyqp3aRNOIVWBHQVhobNE/Mpc7U0H95cXSk1B+TvIZx58vJau9zls7OjMAgAydGd+/VZY1B8VIQfBhXHpd9PqfPzSpMomSVffQ+ju+GiOAZUYzrZkiRtpiU5ejvhQuC2ZK5dmaFD4zjEkUgRS+4JLt5xOOGGZ8qtHTQMLnfKosXG6VzbZjq0yy0R+rsBIBpWES0AECZCBrXuMLi7U7DfgULP/xvawZJxv9dDdJdiMTawRAhm7VK81VmHtuFxr+FgR89XeelWUnnA+Yw5EfbAe6gKYHiT4J5ClwRMWf+8ozV248W9YlQmuBjNFGW2vtx/sbhEYINtM6UTpSp5tcFojyi1VedgblMkT+gj/ed5Bl1796zW143OVkSZYcr+ykcf/Bf/6baK+z9tpDE+vWLzZVlA1WaEQuGCsc+PPjcgUsq15wtbzwtZuy7LDCcA7+mWghRkBEjsgRkBlkChFAlByvHtIs5GHGNEDXJGtxvBZZSx+bTvu9I1ptW29uRKud07ND3OPM59znsuoyh3uzoZCCyXN6tACA4JSdhS9W6r9xhQkGAPlO3H5ve/nb7xW5yIXfvW0SrSOtYz2gODgDwceTLly2gBFABFIEjgidoUiFL1kgRSDHU+MiR+uUAqfsM8HAWrAFM4AWrRaZ4bkBQ6s6/W4/3eyDJRQI4miAsZ8qsJnJWmnzjSf5SSU+AABgMmVTZZVhDndnAnQEsDGTwSJAf84NF31nymOMqX7e+vlWcL3i1Lzb//qT4bWqrLqHkyO8LOVcwAMxnlZcsok2AD20Edh0P8lDwFxRf3lOlCbKljt112l4YAGLxDIN13ciJLAYRUkr27UdjQCy7DqFSRzcjYd9KxOrbC/KdmOdnMi9mMT07m/pflYYDoEcCbkdb/QIJYZLtdL1KeSMlAWEtJks/ePnw6Uq94SJlIkVGQIAHkpvxmu8NDP2jrdLFrAl2MzhZ5qUHuwPAOC+5IUGT4CsleU7GeybfeQMOQNRLLZokXKea5YYppExpxGUrk8dclKO+M5UxKZvr9sTd12gSXS6Z/ZzwOj4cpp5bFytQsGcuudM+7LqIgebadAm72Ymt3kr676/m27HYIEz6wZw5XPzfsPnzvmXAwCYPEw6uxqb5Sj3kDiQLkiFCUs5EJCUVb00j1KrLSBjLpdVz7tRlaGbQg+gGPb9GIYx5nPuCZRDASMdZqCJdKRMX5lEAQTHyowMkCYyRVkWiorLP9cQ/piDDkDMZdUXZ3oftbJuApk1qdn+4UpvM27cbsQbPdXNrCXui8YVLM26ojR+5ddEAj57mxoHuOLQy1Ow2wYNMEzGTwyymqymwuYLVn/lyuxnFpgr0CKjgpxnBEBEQMDMEbqKECwreJBDYfGA4zwGNtMmynWUF2wrA4RQYCggHH/0mMvdaT94tpFsJXkzNrHSmVaZ7X2wy3NdeAhcIntmidfKyMZ3Ssc30SNVYzOEUEIoyZPDCgg2ajnU8SBLOspNrEymAYAImMvdmuvUPOkJJCKyAIRY7GAAJIKjfjS3gltHWGd/KUYyoGOjY33cvim0me3c28maEREBEPdFIN2xncSDx/DF9G/MVW9dcRsh8wQY0u1EbfezdkraIAA5Lnge+T7g+GKaaA0eqRr7MJ1eCBYnCpPIUrYbde/tkLYHx2wUbw1WVyQEy4aBrUWyQ7eZgJjL6nbal8EgeYAABNl20rm3ZzPz9ORTVu0m2U6iOnnhrnOXlz41PaGTCADc5V7Dn//qwtQnZ1EwKvJIREBEAAxAEggCRhMVB00k4FGqsQnQIhHuF0lNvK+WLOWJztOs0OD9TSgDURGiZQiAaDgAIIIIpAjtYS+UO1y8wuQVvu/2ARlr4txEuU0NPtVXN+t90IzuNYtjd7jL5bQvZ3xevoDjWEQovLnAWyqLus8F7ueDAQBQsrLDSy4fsQjrxC7GvnPkY1mIkFlkhDTwcUflf09uEdGgGOTFGYJgUBSmD5WWsKjkISBRcauvXDscR1IA1rPWM0Rm0AiiVVonuY6V1O7w5AYbm/7j9uZfPcn6OSkLgOjw6idmvOnw9IKyEXcCEhAIrD07lT7f2O1lqpMWCsAsuui412acpWkmcBKlmGh2jLZNDYEs0GFeflItRgJGBWsPTDA55cu6VxBD+4wzFcYCAWXgysDl/oFFVZ003Ynb7zZNMijlAQQi6H6w27m/ozp5QVvqVMXb/ebrm/lernNDiETEA8cYsMqo3onEyHAnYOvt7WjljM2ATKAz5TY+OR9cLQPigOJg4JXKldJVbHj0q9LgAlZZFSsi4JLJ8BirhUAMiBMpIgDkHueBFKGcpKQSiVixrDIUZbfyTK28WEWJkBc9HvTNjfRTT+qDBxsUi/3BW2kztrlxZ4IBP6Kt6uVbP3ri1P0K1gAg3YnXfvAoXu2aWONgRqHuZclq+8HPN679k+ePXZiGvqdqZ+23t8PrlRv//MWzNhTRUAdony4gD2ABsAsQIji/Ig0GQMps+4O95T9/lGz2jmeCCLglPqhyJBS8+sK01zjDxJ3WJUNZdYOFUni1LKtesFCqvzQrK3KQrj0kXyIQviizWeE7hz2ntdceFibEv1o6fN1kWu3Fm9/7sPtgb/cna8vffi96v533UiJDQEhI2qpusvHdR8l675RtnGuvPVTtLFrpRCudaLl71oZPpIx69zbS7T7tb4YlDknca39/S32Uj5eUHGIiDUYAk5l0uZu839zY6S793dtsJmQVB4ZWxQD0gPpACQAiETCPsUDyUCAbd2lh4F8JF+7eyZvJ9o9XZckpapdgkMSgob+OBMwT+CXOKke+5sLdW2vfeXDlqzf2fraRNKPDhbMmVulWf+WP3gcLuqdMpocVHwQAwlG7CQ99lOyUwGHh7i01PEul5p6+4ZMU5btp0jSqq8BaREZAZCnv5Dt6HVZ4Y2lezDmyNKZPN3HC3xDmxrTTXjttbtyb/62b8uU5nEbgBABEZHe0/TmZwv2xRNaCnWhKIkNZcWXFdWoeCuw9ah99/yCoIAIoE5SIygeKWviGt7/xav9BK3qwlzbjp2ZZ3s+hP8wnDux30RzzvKnfvEHd5o3fe+4kqztsP1ruNl9fPeskDCRtouUoehyRgYMqWSDLbQ5p853VJMsW/8GNX42ACYC7nIeCuTLfiffSSPxZtx6Whe8RWdXJ1E6aPe7txit5KzdMk6Z0PdK9zERKlieNI0Ug3Jkg7+b7e5xwWG5Fg5Tz8TaiGO5gvuT6rus4WZoBHmYuDyqvjlY7AqJ2/HT+7kv+Ve+UNbVwPJ2qN/Xrs3C6I21Jd1XW7ufdyGoDDLmVRSxvmDKZQa5sNDiOQnWyvJOq9oHLJmuuUz3tSWBiDSb0WOWFme7DvayVqNRu843+m2rp+jOizJuvr2S7SbLVS7r9tB+TApsb7vGN737kzZSS7Wh0uuOEb4Ki7JRuVk2uVSdzqt7Afx7oG51Oi8rQnX5xIX8UaWO0MLgvzsM6O9zgBMX00Vne7ue9pBJW9rXt5Gc+YdyPyIkg3Ux2f7qleqlJdbGKVaJ65vRzqYoA36k70eN2vhcDwPbrq4ebcmruwt3bpzwDTG6imSt4KFnoAGeach1r2GD91bo/GzQ+c1X3VfejneQvIxHIfC8rFklkbPv1FXfaPxdDM/ulpWOv552s+frqzJeWnKpnEx2v9oqCqaJ+ONtNo+UucjYMbQ+gSG9q0SrprG2E3ZflAYZntQyDayCktW7vXlMIZN44BTQFBnJCIE3pZpRs9PPdlIgQgUuWTfXAYSxjRmvh8f7jtuqkxfbzpwZB1s5OQkxedEfcF1ByuMt1J9WdhAtc+879qVfmZ19dcKekbYeB9KLAekLkrdS/Upr+7NXaS7PMP1+u7anJC4PzFtNouStrrnotDa9VrbZZM0YAk2lSFiXjSu29vRlv9JA/XR6LBmzH6oXc2fXTJNY9RcPaDyLuCl52ENGkWvfz/ZWRSJnmD5fbb2+LwBElKXzBnHPXiR7IiSDbjpuvrzCP6V4OwIKZYPrzC+5SZe+DzfRBq/TcbPXONPcFAI1ikD+OC6iq5IGY/sR0/+3tbDsGgHitZwlaf7We3e81XqqrN9coNYwxcsCdCWXNCxYr1RemRcUZ3YtWnWyh5h5efgAg72SP/9O7xeurd287VRcAbGY77zW7j/ZUOwVrneuV2c8tejX/lMZNrLf+crn3YUv38sIzY5y5U37j8wtO1d/8/mNa7x76OJnM2L3YGhFWylMv1Pm0PFecekROFvJW7DTkxv/6qPPLPebK0q/P1j+76Ey7pRvV9nNt4Yja89MiGP/kxAsQsPCFPxcKyWTJVb1MVj3QNmslJlXx+i6C1YkBBOCICCiQzl81O+DLrh25qDqZU331qWSlzUx4szrdTvu/bHbe3Kg/N1P/xJxoeKc0riPFfbHynUfJWheMBWOcqtv49MLcl2/oTHcftk2mdXxQsYUIwBF0JtoQsor7QoDhuHQCQ1n1wd8SNQoXqyCFmAlkzRWBg5I3yg4AoJyIqryYumhZcm783ouP/uAt3VWWir02pFKl911SKjJKRboEL2bv9LFkOHO56/pOzQNtZTOpTAfcl085RE8RxSKQ3kww9dyMXJyGrT2wOliszHxxSdZdlojGK3PJatfEGsDC4GRLAG1Nlne9tZJ2HX0DYfz1mMAEV2YWvl7Jmlm80q+/PIsuIyAmGZuMpCxwQQKuusE1eO4bn27+ZLXz/o7q5gfnkB12UQQKX4pAMMEvSsbHv8HAvxIGv3sbOT61Y/rYIgVZdWf/zlK9r4jm0BhRdkXJYS5HzryZkj87pXq5zdTwCDUkJrnAEkDZgjtJ7oSYEO5Uya2VvIaqPj9TpCMnaPBpjHrmQ/Hi9OCPe2L+689UPzGz9qcPk/XIRKr4uYsBE0SEgoLrYbhUG3Gb+thAhqJ2jFk+/nx0BB5KHoLbePrbIUNvNph+cVZvRJnqaGuKyAkZeH64cO3Z4NnKxegIAh+tSO28J1aebQRGPyWRudydDkrPTC38/dvBYllOeXgo1UVA2iVTYRhydv49NheF8x0Zx8Ba418PFu40yo2yKDm4n3iW1wLnCyW3VmJizNK7MTDGiZVnDPQYpySKkizdrN74p7/W+OxVby4UJbfYBMYYYijzKnDv0ne8wcmH1p/ryDjVyZL17uNvv21v+dO/cz2YrbBQEgKvSH6F8TlBwd+SaGHcEyvPHuvznpJYZHuYJ+Yr16svNLZ+uGp6WVGu7C2UZn/txhiB43lxUjXguX475rA93/zpk2d+/6W5ac/+2TJ1U1n1Zj97/TJ+neN0jHFi5Rm/mzTh8f6qn+u+0v0ciJChKDuy5Iy42IyNw4IJr1XvfOPV8Q4cjFY6D775Zuvtbafq3fnGq9UXZ4Az3czMXxt5R/DbzqWedPdxjCeLM+bghD+XJEuOLDkA4XlvnBCT/zyP6mTRcjda7gJAeL0SXK84Ux4AOMKBuwAAEFzIk54D48li1F8++38O3/v8tyb8Cb7/D37KDwD+D/oTgQhYIXfMAAAAAElFTkSuQmCC'}
    '''
    # 生成验证码
    code = operate_captcha.generate_code()
    # 生成图片验证码
    image_base64_str = operate_captcha.generate_captcha_base64(code)

    # 生成唯一key
    code_key = operate_captcha.generate_code_key()

    # 存入Redis
    redis_db.set(code_key, code.casefold(), 60*2)

    data = {
        "code_key": code_key,
        "code_img": image_base64_str
    }
    print(data)
    return data
