<?php

declare(strict_types=1);
/**
 * @copyright 2021 Andrey Borysenko <andrey18106x@gmail.com>
 * @copyright 2021 Alexander Piskun <bigcat88@icloud.com>
 *
 * @author Andrey Borysenko <andrey18106x@gmail.com>
 *
 * @license GNU AGPL version 3 or any later version
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

namespace OCA\MediaDC\Controller;

use OCA\Files\Event\LoadSidebar;
use OCA\MediaDC\AppInfo\Application;
use OCA\Viewer\Event\LoadViewer;
use OCP\App\IAppManager;
use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\TemplateResponse;
use OCP\AppFramework\Http\ContentSecurityPolicy;
use OCP\AppFramework\Services\IInitialState;
use OCP\EventDispatcher\IEventDispatcher;
use OCP\IConfig;
use OCP\IRequest;
use OCP\IUserSession;
use OCP\Util;


class PageController extends Controller {

	/** @var IEventDispatcher */
	private $eventDispatcher;

	public function __construct(IRequest $request,
								IEventDispatcher $eventDispatcher) {
		parent::__construct(Application::APP_ID, $request);

		$this->eventDispatcher = $eventDispatcher;
	}

	/**
	 * @NoAdminRequired
	 * @NoCSRFRequired
	 * Render default index template
	 *
	 * @return TemplateResponse
	 */
	public function index(): TemplateResponse {
		$this->eventDispatcher->dispatchTyped(new LoadSidebar());
		$this->eventDispatcher->dispatchTyped(new LoadViewer());

		Util::addScript(Application::APP_ID, 'mediadc-main');

		$response = new TemplateResponse(Application::APP_ID, 'main');

		$policy = new ContentSecurityPolicy();
		$policy->addAllowedWorkerSrcDomain("'self'");
		$policy->addAllowedScriptDomain("'self'");
		$response->setContentSecurityPolicy($policy);

		return $response;
	}
}
