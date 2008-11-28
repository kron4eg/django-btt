# -*- coding: utf-8 -*-

from cgi import parse_qsl

from django.conf import settings
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError

from lib import render_to
from lib.bt.bencoding import encode, decode
from torrent.models import Torrent
from tracker.models import Peer

@render_to('btt/base.html')
def announce(request):
    qs = dict(parse_qsl(request.META['QUERY_STRING']))
    if qs.get('info_hash') is None:
        return {}
    info_hash = qs['info_hash'].encode('hex')
    responce_dict = {'interval': settings.ANNOUNCE_INTERVAL}
    try:
        torrent = Torrent.objects.get(info_hash=info_hash)
    except Torrent.DoesNotExist:
        responce_dict['failure reason'] = 'torrent not redistered'
        responce_dict['interval'] = 3600
        return HttpResponse(encode(responce_dict))

    try:
        ip = request.META['REMOTE_ADDR']
        port = request.GET['port']
        peer_id = request.GET['peer_id']
        uploaded = request.GET['uploaded']
        downloaded = request.GET['downloaded']
        left = request.GET['left']
        compact = request.GET.get('compact', 0)
        event = request.GET.get('event')
    except MultiValueDictKeyError:
        responce_dict['failure reason'] = 'invalid request'
        responce_dict['interval'] = 600
        return HttpResponse(encode(responce_dict))

    if 'started' in event:
        peer, created = Peer.objects.get_or_create(peer_id=peer_id, port=port, ip=ip, torrent=torrent)
        if created:
            peer.save()
    elif 'stopped' in event:
        try:
            peer = Peer.objects.get(peer_id=peer_id, ip=ip, torrent=torrent)
            peer.delete()
        except Peer.DoesNotExist:
            pass
    elif 'completed' in event:
        pass

    return HttpResponse(encode(responce_dict))
