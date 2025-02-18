import { Resolver, Query, Mutation, Args } from '@nestjs/graphql';
import { WebsocketService } from './websocket.service';
import { CreateWebsocketInput } from './dto/create-websocket.input';
import { UpdateWebsocketInput } from './dto/update-websocket.input';

@Resolver('Websocket')
export class WebsocketResolver {
  constructor(private readonly websocketService: WebsocketService) {}

  @Mutation('createWebsocket')
  create(@Args('createWebsocketInput') createWebsocketInput: CreateWebsocketInput) {
    return this.websocketService.create(createWebsocketInput);
  }

  @Query('websocket')
  findAll() {
    return this.websocketService.findAll();
  }

  @Query('websocket')
  findOne(@Args('id') id: number) {
    return this.websocketService.findOne(id);
  }

  @Mutation('updateWebsocket')
  update(@Args('updateWebsocketInput') updateWebsocketInput: UpdateWebsocketInput) {
    return this.websocketService.update(updateWebsocketInput.id, updateWebsocketInput);
  }

  @Mutation('removeWebsocket')
  remove(@Args('id') id: number) {
    return this.websocketService.remove(id);
  }
}
