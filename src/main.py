from argparse import ArgumentParser

import CDDB, DiscID
import audiotools


if __name__ == '__main__':
    ap = ArgumentParser()
    ns = ap.parse_args()

    while True:
        cdrom = DiscID.open()
        disc_id = DiscID.disc_id(cdrom)

        query_status, results = CDDB.query(disc_id)
        stored_results = {}

        print query_status, results

        # Hack because I suck at coding
        if isinstance(results, dict):
            results = [results]

        for i, query_info in enumerate(results):
            print " == RESULT %d ==" % i
            read_status, read_info = CDDB.read(query_info['category'], query_info['disc_id'])
            print read_status, read_info
            stored_results[i] = read_info

            for tn in range(disc_id[1]):
                print "Track %.02d: %s" % (tn+1, read_info['TTITLE%d' % tn])

        if len(results) > 1:
            result = raw_input("Select a result: ")
            result = int(result)
            assert result <= len(results), result
            assert result >= 0, result
            print "Using Result #%d" % result
            result = stored_results[result]
        elif len(results) == 1:
            result = stored_results[0]
        else:
            assert False,"No results make me sad"

        atcd = audiotools.CDDA(cdrom.name)
        for i in range(disc_id[1]):
            tn = i + 1
            track = result['TTITLE%d' % i]
            artist, album = result['DTITLE'].split(' / ', 1)

            output_filename = "%s - %s - %s.mp3" % (artist, album, track)
            print output_filename
            audiotools.MP3Audio.from_pcm(output_filename, atcd[tn])

        result = raw_input("Press Enter to Continue")
